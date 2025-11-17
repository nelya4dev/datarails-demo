class L:
    """
    Field length constants.

    Short class name 'L' for convenience in imports: String(L.EMAIL)
    """

    # ==================== Names & Identity ====================
    NAME_SHORT = 50         # username, handle, display_name
    NAME_STANDARD = 100     # first_name, last_name, middle_name, group_name
    NAME_FULL = 300         # full_name (first + middle + last + spaces)
    EMAIL = 320             # RFC 5321 max email length
    PHONE = 20              # International format (+XXX XXXX XXXX)

    # ==================== Text Content ====================
    TITLE = 200             # Titles, headings, subjects, dictionary names, group names
    SUBTITLE = 500          # Taglines, summaries, short descriptions, dictionary descriptions
    # For long content (articles, posts, full descriptions), use Text type (unlimited)

    # ==================== URLs & Paths ====================
    URL = 2048              # Max browser URL length
    SLUG = 150              # URL-friendly identifiers
    DOMAIN = 253            # Max DNS domain length
    PATH = 500              # File paths, URI paths

    # ==================== Security & Tokens ====================
    HASH = 64               # SHA256 hash (most common)
    HASH_BCRYPT = 60        # Bcrypt output (actual length is 60 chars)
    PASSWORD = 255          # User password in transit (before hashing)
    TOKEN = 255             # OAuth tokens, API keys
    TOKEN_LONG = 512        # JWT with many claims
    UUID_STR = 36           # UUID with hyphens (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)

    # ==================== OAuth2 & Auth ====================
    CLIENT_ID = 128         # OAuth2 client_id
    CLIENT_SECRET = 64      # OAuth2 client_secret (hashed with SHA256)
    SCOPE = 500             # Space-separated scopes
    GRANT_TYPE = 50         # OAuth grant type

    # ==================== Codes & Identifiers ====================
    CODE = 50               # General codes (status, type, SKU)
    REFERENCE = 100         # Reference numbers, IDs
    LANGUAGE = 10           # Language code (en-US)
    COUNTRY = 2             # Country code (US)
    CURRENCY = 3            # Currency code (USD)

    # ==================== Request Metadata ====================
    USER_AGENT = 500        # Browser/client user agent
    IP_ADDRESS = 45         # IPv6 max length (8 groups of 4 hex digits + 7 colons)


def print_lengths():
    """Print formatted table of all field length constants for reference.

    Outputs a nicely formatted table showing all L class constants organized
    by category (Names, URLs, Security, etc.). Useful for developers to quickly
    look up appropriate field lengths when defining new models or schemas.

    Categories Displayed:
        - Names & Identity: username, email, phone
        - Text Content: titles, subtitles
        - URLs & Paths: URLs, slugs, domains
        - Security & Tokens: hashes, passwords, tokens
        - OAuth2 & Auth: client IDs, secrets, scopes
        - Codes & Identifiers: status codes, references
        - Request Metadata: user agents, IP addresses

    Output Format:
        For each constant, displays: name, value (length), and description.
        Example: "L.EMAIL              320   RFC 5321 max email length"

    Note:
        This function is primarily for development reference and debugging.
        The constants should be used directly in code via the L class.
    """
    print("\n" + "=" * 80)
    print(" DATABASE FIELD LENGTH STANDARDS".center(80))
    print("=" * 80 + "\n")

    sections = {
        "Names & Identity": [
            ("NAME_SHORT", "username, handle, display_name"),
            ("NAME_STANDARD", "first_name, last_name, middle_name"),
            ("NAME_FULL", "full_name (first + middle + last)"),
            ("EMAIL", "RFC 5321 max email length"),
            ("PHONE", "International format"),
        ],
        "Text Content": [
            ("TITLE", "Titles, headings, dictionary names"),
            ("SUBTITLE", "Descriptions, summaries"),
            ("Text type", "Use for unlimited content (import from sqlalchemy)"),
        ],
        "URLs & Paths": [
            ("URL", "Max browser URL length"),
            ("SLUG", "URL-friendly identifiers"),
            ("DOMAIN", "Max DNS domain length"),
            ("PATH", "File paths, URI paths"),
        ],
        "Security & Tokens": [
            ("HASH", "SHA256 hash"),
            ("HASH_BCRYPT", "Bcrypt output"),
            ("PASSWORD", "User password (before hashing)"),
            ("TOKEN", "OAuth tokens, API keys"),
            ("TOKEN_LONG", "JWT with many claims"),
            ("UUID_STR", "UUID with hyphens"),
        ],
        "OAuth2 & Auth": [
            ("CLIENT_ID", "OAuth2 client_id"),
            ("CLIENT_SECRET", "OAuth2 client_secret (hashed)"),
            ("SCOPE", "Space-separated scopes"),
            ("GRANT_TYPE", "OAuth grant type"),
        ],
        "Codes & Identifiers": [
            ("CODE", "General codes (status, type)"),
            ("REFERENCE", "Reference numbers, IDs"),
            ("LANGUAGE", "Language code (en-US)"),
            ("COUNTRY", "Country code (US)"),
            ("CURRENCY", "Currency code (USD)"),
        ],
        "Request Metadata": [
            ("USER_AGENT", "Browser/client user agent"),
            ("IP_ADDRESS", "IPv6 max length"),
        ],
    }

    for section_name, fields in sections.items():
        print(f"\n{section_name}:")
        for field_name, description in fields:
            if field_name == "Text type":
                print(f"  {'Text':<20} {'∞':>6}   {description}")
            else:
                value = getattr(L, field_name, "N/A")
                print(f"  L.{field_name:<18} {str(value):>6}   {description}")

    print("\n" + "=" * 80)
    print("\nUsage:")
    print("  from backend.db.lengths import L")
    print("  from sqlalchemy import String, Text")
    print("  ")
    print("  name: Mapped[str] = mapped_column(String(L.NAME_STANDARD))")
    print("  description: Mapped[str] = mapped_column(Text)")
    print("  ")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    # Print lengths when run as script
    print_lengths()
