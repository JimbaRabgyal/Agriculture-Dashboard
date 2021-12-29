mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "
[theme]
primaryColor = "#ffffff"
backgroundColor = "#ccdede"
secondaryBackgroundColor = "#99cccc"
textColor = "#010100"
font = "sans serif"
[server]
headless = true
enableCORS=false
port = $PORT
" > ~/.streamlit/config.toml
