#!/usr/bin/env python3
"""Server configuration example with advanced validation."""

import robust_input as ri

def validate_port(port_str: str) -> bool:
    """Validate port number and check if it's not reserved."""
    try:
        port = int(port_str)
        if port < 1024:
            return False  # Reserved ports
        if port > 65535:
            return False  # Invalid port range
        return True
    except ValueError:
        return False

def main():
    print("🖥️  Server Configuration Setup")
    print("=" * 35)
    
    # Server details
    hostname = ri.get_input(
        prompt="🌐 Server Hostname",
        pattern=r'^[a-zA-Z0-9.-]+$',
        min_length=3,
        max_length=253,
        default="localhost",
        prompt_style=[ri.InputStyle.CYAN, ri.InputStyle.BOLD],
        error_message="❌ Invalid hostname format"
    )
    
    ip_address = ri.get_ip_address(
        prompt="🔗 IP Address",
        default="127.0.0.1",
        prompt_style=[ri.InputStyle.CYAN, ri.InputStyle.BOLD]
    )
    
    port = ri.get_input(
        prompt="🚪 Port Number",
        target_type=int,
        default="8080",
        custom_validator=validate_port,
        prompt_style=[ri.InputStyle.CYAN, ri.InputStyle.BOLD],
        error_message="❌ Port must be between 1024-65535"
    )
    
    # SSL Configuration
    enable_ssl = ri.get_input(
        prompt="🔒 Enable SSL",
        target_type=bool,
        default="false",
        prompt_style=[ri.InputStyle.YELLOW, ri.InputStyle.BOLD],
        error_message="❌ Please enter yes/no or true/false"
    )
    
    if enable_ssl:
        ssl_cert = ri.get_input(
            prompt="📄 SSL Certificate Path",
            pattern=r'^[^<>:"|?*]+\.pem$',
            default="/etc/ssl/certs/server.pem",
            prompt_style=[ri.InputStyle.YELLOW],
            error_message="❌ Certificate must be a .pem file"
        )
    else:
        ssl_cert = None
    
    # Database configuration
    db_type = ri.get_choice(
        prompt="🗄️  Database Type",
        choices=["postgresql", "mysql", "sqlite", "mongodb"],
        default="postgresql",
        prompt_style=[ri.InputStyle.GREEN, ri.InputStyle.BOLD]
    )
    
    # Worker configuration
    workers = ri.get_integer(
        prompt="👥 Worker Processes",
        min_value=1,
        max_value=32,
        default=4,
        prompt_style=[ri.InputStyle.MAGENTA, ri.InputStyle.BOLD],
        error_message="❌ Workers must be between 1 and 32"
    )
    
    # Generate configuration summary
    print("\n📋 Configuration Summary:")
    print("=" * 30)
    print(f"Hostname: {hostname}")
    print(f"IP Address: {ip_address}")
    print(f"Port: {port}")
    print(f"SSL Enabled: {'Yes' if enable_ssl else 'No'}")
    if ssl_cert:
        print(f"SSL Certificate: {ssl_cert}")
    print(f"Database: {db_type}")
    print(f"Workers: {workers}")
    
    # Confirmation
    confirm = ri.get_input(
        prompt="💾 Save configuration",
        target_type=bool,
        default="yes",
        prompt_style=[ri.InputStyle.BRIGHT_GREEN, ri.InputStyle.BOLD],
        error_message="❌ Please enter yes/no"
    )
    
    if confirm:
        print("✅ Configuration saved successfully!")
    else:
        print("❌ Configuration discarded.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Configuration cancelled.")