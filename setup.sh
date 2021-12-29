mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml

echo "[theme]
primaryColor="#35793b"
backgroundColor="#ccdede"
secondaryBackgroundColor="#99cccc"
textColor="#010100"
" > ~/.streamlit/config.toml


