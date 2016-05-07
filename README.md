# gateway
Safely expose internal service to the Internet.

## What is it
As its name indicates, `gateway` is an application gateway for safely expose
 internal services to the Internet.

Some services don't have an account system or any kind of verification, so
 you can't just expose them to the Internet. It might be a monitoring service,
 or just a bunch of small web projects running on your server for which you
 don't want to re-implement account system one by one. For these applications,
 `gateway` provides unified account system and verification.

## How does it work
`Gateway` sits between nginx and your web applications. When a request reaches
 the endpoint configured for one of your applications, it actually hit
 `gateway`. If the request passed account verification, `gateway` then fetches
 the desired service resources (HTML page / JSON data, etc.) from your
 application, and return it to the client.

You can think of it as an HTTP proxy server with authentication, the only
 difference being it deployed on the same server as your web application.

## Data storage
All data (user accounts / service configurations) is stored on LeanCloud,
 you don't need to mess with any kind of database on your server. Just create
 an application on LeanCloud, copy and paste the app id and app key into
 the configuration file.

## How to use
`Gateway` is currently under early construction. Deployment instructions will
 be available once the first release comes out.

## License
BSD license, see LICENSE file for details.
Please notice that `gateway` is a commonly used word, it's a project name, not
 a product name.

