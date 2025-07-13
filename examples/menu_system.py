#!/usr/bin/env python3
"""Interactive menu system with dynamic choices."""

import robust_input as ri

class MenuSystem:
    def __init__(self):
        self.running = True
        self.data = {}
    
    def main_menu(self):
        """Display main menu and handle choice."""
        while self.running:
            print("\n🔧 System Administration Tool")
            print("=" * 35)
            
            choice = ri.get_choice(
                prompt="Select an option",
                choices=["users", "files", "network", "logs", "quit"],
                prompt_style=[ri.InputStyle.BRIGHT_BLUE, ri.InputStyle.BOLD],
                error_message="❌ Please select a valid option"
            )
            
            if choice == "users":
                self.user_management()
            elif choice == "files":
                self.file_operations()
            elif choice == "network":
                self.network_config()
            elif choice == "logs":
                self.log_viewer()
            elif choice == "quit":
                self.running = False
                print("👋 Goodbye!")
    
    def user_management(self):
        """User management submenu."""
        print("\n👥 User Management")
        
        action = ri.get_choice(
            prompt="Choose action",
            choices=["add", "delete", "modify", "list", "back"],
            prompt_style=[ri.InputStyle.GREEN]
        )
        
        if action == "add":
            username = ri.get_input(
                prompt="Username",
                pattern=r'^[a-zA-Z0-9_]{3,20}$',
                error_message="❌ Username: 3-20 chars, letters/numbers/underscore only"
            )
            
            is_admin = ri.get_input(
                prompt="Admin privileges",
                target_type=bool,
                default="false",
                error_message="❌ Please enter yes/no"
            )
            
            print(f"✅ User '{username}' created (Admin: {is_admin})")
    
    def file_operations(self):
        """File operations submenu."""
        print("\n📁 File Operations")
        
        operation = ri.get_choice(
            prompt="Choose operation",
            choices=["backup", "restore", "cleanup", "permissions", "back"],
            prompt_style=[ri.InputStyle.YELLOW]
        )
        
        if operation in ["backup", "restore"]:
            path = ri.get_input(
                prompt="File/Directory path",
                pattern=r'^(/[^/ ]*)+/?$',
                default="/home",
                error_message="❌ Please enter a valid Unix path"
            )
            print(f"✅ {operation.title()} scheduled for: {path}")
    
    def network_config(self):
        """Network configuration submenu."""
        print("\n🌐 Network Configuration")
        
        config_type = ri.get_choice(
            prompt="Configuration type",
            choices=["interface", "firewall", "dns", "routing", "back"],
            prompt_style=[ri.InputStyle.CYAN]
        )
        
        if config_type == "interface":
            interface = ri.get_input(
                prompt="Interface name",
                pattern=r'^(eth|wlan|lo)\d+$',
                default="eth0",
                error_message="❌ Format: eth0, wlan0, lo0, etc."
            )
            
            ip = ri.get_ip_address(
                prompt="IP Address",
                default="192.168.1.100"
            )
            
            print(f"✅ Interface {interface} configured with IP {ip}")
    
    def log_viewer(self):
        """Log viewer submenu."""
        print("\n📊 Log Viewer")
        
        log_type = ri.get_choice(
            prompt="Log type",
            choices=["system", "application", "security", "custom", "back"],
            prompt_style=[ri.InputStyle.MAGENTA]
        )
        
        if log_type != "back":
            lines = ri.get_integer(
                prompt="Number of lines",
                min_value=10,
                max_value=1000,
                default=50,
                error_message="❌ Lines must be between 10 and 1000"
            )
            
            print(f"📄 Displaying last {lines} lines of {log_type} log...")

def main():
    menu = MenuSystem()
    try:
        menu.main_menu()
    except KeyboardInterrupt:
        print("\n⚠️  Application terminated by user.")

if __name__ == "__main__":
    main()