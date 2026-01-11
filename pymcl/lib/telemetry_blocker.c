#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <arpa/inet.h>
#include <errno.h>

// Function pointer type for the real getaddrinfo
typedef int (*getaddrinfo_t)(const char *node, const char *service,
                             const struct addrinfo *hints,
                             struct addrinfo **res);

// List of domains to block (suffixes)
const char *BLOCKED_DOMAINS[] = {
    "vortex.data.microsoft.com",
    "settings-win.data.microsoft.com",
    "telemetry.minecraft.net",
    "snooper.minecraft.net",
    "pie.optimizely.com", // used for A/B testing/tracking, so why not?
    NULL
};

#define ANSI_CYAN "\033[0;36m"
#define ANSI_RED "\033[0;31m"
#define ANSI_RESET "\033[0m"

__attribute__((constructor))
void setup(void) {
    fprintf(stderr, "%s[PyMCL] Telemetry Blocker Injected (v1.0)%s\n", ANSI_CYAN, ANSI_RESET);
}

int is_blocked(const char *node) {
    if (!node) return 0;
    for (int i = 0; BLOCKED_DOMAINS[i] != NULL; i++) {
        // Check if node ends with the blocked domain
        size_t node_len = strlen(node);
        size_t blocked_len = strlen(BLOCKED_DOMAINS[i]);
        
        if (node_len >= blocked_len) {
            if (strcmp(node + node_len - blocked_len, BLOCKED_DOMAINS[i]) == 0) {
                return 1;
            }
        }
    }
    return 0;
}

int getaddrinfo(const char *node, const char *service,
                const struct addrinfo *hints,
                struct addrinfo **res) {
    
    if (is_blocked(node)) {
        fprintf(stderr, "%s[PyMCL] 🛡️ BLOCKED connection to: %s%s\n", ANSI_RED, node, ANSI_RESET);
        
        struct addrinfo *info = (struct addrinfo *)calloc(1, sizeof(struct addrinfo));
        if (!info) return EAI_MEMORY;
        
        // Mimic hints if provided, otherwise default to IPv4
        info->ai_family = AF_INET;
        info->ai_socktype = hints ? hints->ai_socktype : SOCK_STREAM;
        info->ai_protocol = hints ? hints->ai_protocol : IPPROTO_TCP;
        
        struct sockaddr_in *sa = (struct sockaddr_in *)calloc(1, sizeof(struct sockaddr_in));
        if (!sa) {
            free(info);
            return EAI_MEMORY;
        }
        
        sa->sin_family = AF_INET;
        if (service) {
             // Simple port parsing, usually not strictly necessary for simple blocking
             sa->sin_port = htons(atoi(service)); 
        }
        inet_pton(AF_INET, "0.0.0.0", &(sa->sin_addr));
        
        info->ai_addr = (struct sockaddr *)sa;
        info->ai_addrlen = sizeof(struct sockaddr_in);
        info->ai_canonname = node ? strdup(node) : NULL;
        
        *res = info;
        return 0;
    }

    // Load real getaddrinfo
    static getaddrinfo_t real_getaddrinfo = NULL;
    if (!real_getaddrinfo) {
        real_getaddrinfo = (getaddrinfo_t)dlsym(RTLD_NEXT, "getaddrinfo");
    }
    
    return real_getaddrinfo(node, service, hints, res);
}
