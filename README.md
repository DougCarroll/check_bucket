# check_bucket

## Using ngrok to expose application to Internet

1. Install ngrok using the package manager of your choice

`brew install ngrok`

2. Retrieve your Authtoken from ngrok by visiting https://dashboard.ngrok.com/get-started/your-authtoken

3. Add your Authtoken to the conguration file

`ngrok config add-authtoken <Your Authtoken>`

4. Setup the tunnel

`ngrok http 9000`

5. Launch and run the app as normal. In addition to localhost, it will also be available at the Forwarded address setup by ngrock
