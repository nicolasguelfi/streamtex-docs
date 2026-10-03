from streamtex import st_book, ExportConfig, ExportMode, AssetMode

config = ExportConfig(
    enabled=True,                    # Enable/disable export
    page_title="My Document",        # <title> tag
    page_width="100%",             # Page width in export
    page_padding="36pt",             # Page padding/margins
    format="html",                   # "html" or "pdf"
    mode=ExportMode.ALWAYS,          # ALWAYS, MANUAL or NEVER
    output_dir="./exports",          # Where the file is written
    filename="my-document",          # Output file name (no extension)
    asset_mode=AssetMode.EMBEDDED,   # Embed images as base64 (EXTERNAL: data/ folder)
)

st_book([...], exports=[config])
