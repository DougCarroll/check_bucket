# check_bucket

## Using ngrok to expose application to Internet

1. Install ngrok using the package manager of your choice

`brew install ngrok`

2. Retrieve your Authtoken from ngrok by visiting 

https://dashboard.ngrok.com/get-started/your-authtoken

3. Add your Authtoken to the conguration file

`ngrok config add-authtoken <Your Authtoken>`

4. Setup the tunnel

`ngrok http 9000`

5. Launch and run the app as normal. In addition to localhost, it will also be available at the Forwarded address setup by ngrok

![Screenshot 2023-03-31 at 7 53 37 AM](https://user-images.githubusercontent.com/23019517/229155515-1db3d420-a384-4d4b-b373-80b0fbb82db9.png)
