#Proxy

A Corporate Proxy Server filters web content and malicious software.  It also improves performance of frequently accessed web pages.

Web Browsers get their proxy info from the network settings.  Some companies have a http script (pac.pac file) that helps the 
browser know which URLs are internal vs. external.  Firefox allows for manual configuration as well.

When using Predix and/or the Reference App it depends on your situation whether to set or unset the Proxy config.  Tools such as wget, curl, git, maven etc use the Environment variables such as
- HTTP_PROXY=http://proxy.mycompany.com:8080
- HTTPS_PROXY=http://proxy.mycompany.com:8080
- http_proxy=http://proxy.mycompany.com:8080
- https_proxy=http://proxy.mycompany.com:8080
- no_proxy=mycompany.com

Thus if you are on your Corporate Network or over VPN to your Corporate Network the proxy is required to get to servers out on the Internet and you MUST have these env vars set.  If you are at home or a cafe on the public internet and not using VPN then you MUST unset these variables because the proxy server will not be found.

>While most ENV vars are upper case it's an historical oddity that http_proxy is defined in lower case.  Thus, both lower and upper case
env vars are often set.  The noproxy env var tells the tool to not bother going to the proxy server for certain domains, usually internal
to the network.

On OSX or linux this will unset it for the current terminal window
- unset HTTP_PROXY
- unset HTTPS_PROXY
- unset http_proxy
- unset https_proxy

On Windows this will unset it for the current command window
- set HTTP_PROXY=
- set HTTPS_PROXY=
- set http_proxy=
- set https_proxy=
