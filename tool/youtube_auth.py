#!/usr/bin/env python3
"""One-time setup: get a YouTube refresh token for youtube_upload.py.

Run it on your PC (it opens a browser so you can sign in with the Google account that owns @tunzlequiz):

  python youtube_auth.py CLIENT_ID CLIENT_SECRET

It prints the refresh token. Save the three values as GitHub secrets
YT_CLIENT_ID, YT_CLIENT_SECRET and YT_REFRESH_TOKEN (see README).
"""
import http.server, secrets, sys, threading, urllib.parse, webbrowser
import requests

SCOPE = "https://www.googleapis.com/auth/youtube.upload"
PORT = 8765


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    client_id, client_secret = sys.argv[1], sys.argv[2]
    redirect = f"http://127.0.0.1:{PORT}/"
    state = secrets.token_urlsafe(16)
    got = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if q.get("state", [""])[0] == state:
                got.update({k: v[0] for k, v in q.items()})
            self.send_response(200); self.send_header("Content-Type", "text/plain; charset=utf-8"); self.end_headers()
            self.wfile.write("Done. You can close this tab and go back to the terminal.".encode())
            threading.Thread(target=self.server.shutdown).start()

        def log_message(self, *a): pass

    srv = http.server.HTTPServer(("127.0.0.1", PORT), H)
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": client_id, "redirect_uri": redirect, "response_type": "code", "scope": SCOPE,
        "access_type": "offline", "prompt": "consent", "state": state})
    print("Opening your browser. If it doesn't open, visit:\n" + url + "\n")
    webbrowser.open(url)
    srv.serve_forever()

    if "code" not in got:
        sys.exit("No code received: " + str(got))
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "code": got["code"], "client_id": client_id, "client_secret": client_secret,
        "redirect_uri": redirect, "grant_type": "authorization_code"}, timeout=30)
    r.raise_for_status()
    tok = r.json()
    if "refresh_token" not in tok:
        sys.exit("Google returned no refresh token. Remove the app's access at https://myaccount.google.com/permissions and run this again.")
    print("YT_REFRESH_TOKEN =", tok["refresh_token"])


if __name__ == "__main__":
    main()
