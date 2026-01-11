#!/bin/bash
set -e

echo "Starting dbt container..."

# Install dependencies
echo "Installing dbt dependencies..."
dbt deps

# Check if target/index.html exists (docs already generated)
if [ ! -f target/index.html ]; then
    echo "Docs not found. Creating placeholder..."
    mkdir -p target
    # Create a simple placeholder
    cat <<EOF > target/index.html
<!DOCTYPE html>
<html>
<head>
    <title>dbt Docs</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding-top: 50px; }
        .container { max-width: 600px; margin: 0 auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>dbt Docs not generated yet</h1>
        <p>The container has started.</p>
        <p>To generate the full documentation, please run:</p>
        <code>docker compose exec dbt dbt docs generate</code>
        <p>Refresh this page afterwards.</p>
    </div>
</body>
</html>
EOF
fi

# Serve docs (blocking command)
echo "Starting dbt docs server on port 8081..."
exec dbt docs serve --port 8081 --host 0.0.0.0 --no-browser
