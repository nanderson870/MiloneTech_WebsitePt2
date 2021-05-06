# Introduction
Hello. If you are reading this it's because you've been chosen to work on an expansion to the MiloneTech Website.

There will be a learning curve associated with working on this website, as there was for my group when we inherited the project from the previous group. I will do my best to explain how it works, but research will be necessary. There are more than enough resources online to learn what's going on, and trial and error in modifying our code will bolster your understanding immensely.

This website is built as a REST-ful API. This is perhaps the most important concept to understand: the definition of a REST-ful API is that it's an architectural style that uses GET, PUT, POST, and DELETE requests to communicate and manage data. In our case, this means that the server and the client communicate via these methods. More on how these work below.


# General Structure
There are effectively three main components of the website: the database, the client view, and the server. These effectively form a model, view, controller architecture, where the database forms the structure of the data, the client view is the webpage the user sees, and the server manages the interaction between the two.

The database is an SQL Database
The client view is a set of webpages formatted in HTML and CSS, their functionality programmed in JavaScript
The server is set up on the AWS, and it mostly consists of Python


# The Client View
The client view consists of all of the '.html' files. These dictate the layout of the pages. Many of them "extend" other html files using Jinja2, which I will discuss in more detail further down. Essentially this works like extending in any other language. The base page that is extended by others is rendered first, and content from pages that extend that page is filled in in designated places.

In base.html, which most of the pages extend, the CSS style, and multiple scripts, are defined, and as such the rest of the pages that extend base.html also use it's CSS style and can call it's scripts. CSS files match each element in the HTML to entries in them, which contain details about how to display those elements. Whatever specifications are listed are applied to the element on the page.

The client view can most easily communicate with the server by sending GET/POST requests to it. HTML can handle links fairly trivially, but if, for example, you needed to get content without leaving the page, you could associate the clicking of a button (or any other number of actions) with a JavaScript function in which you would send a GET or POST (depending on what you need) request to "usersmilonetech.com/<one of the routes in routes.py>", optionally sending data to the server. The server, in routes.py, would then parse the url, and you could have it parse the data and return it's own data, which you would handle in a function in the JavaScript that receives the response to the request you sent.


# The Server
The server runs on the EC2 virtual machine on AWS. The domain name 'usersmilonetech.com' routes traffic to the IP of the EC2, and then NGINX takes the traffic and redirects it into our Flask application. All of that is more or less automatic, and you're unlikely to need to learn about that. But the next part is important: the Flask application filters the traffic through routes.py, which handles everything appended to the URL, returning the html document that we wish to associate with the url.

For example: a user enters "http://usersmilonetech.com/home" into their address bar. This is a GET request. "usersmilonetech.com" gets rerouted to the IP of the EC2, and the entire url entered gets sent to NGINX. NGINX redirects this to "https://usersmilonetech.com/home" (changes it from http to https), then sends the request to the server that the Flask application is running on (some port on the EC2). routes.py parses the "/login" part of the request - so now the function under @app.route("/home") gets called. (Also note the @login_required, this just requires that the user is logged in to visit this page). This function initializes a bunch of data and then returns a 'render_template' using home.html and the data.

render_templates are an easy way to get custom data into an html document. Normally, when we return an HTML document, it sends a predefined page to the user. The page may need certain data (like the user's name to display in a hello message) from the server. It could get this data by sending a get request in its' JavaScript, but the soonest that could happen is once the page was loaded, and after the time it takes for the script to run. Flask is capable of using render_templates, instead. It uses a 'templating language' called Jinja2 to insert variable data into an HTML page.

So to return to our earlier example, when @app.route("/home") returns render_template('home.html', account_info=current_user.user_data), we can reference account_info in home.html using Jinja2. {{account_info.name}} in the HTML, for instance, would display exactly like current_user.user_data["name"] in the Python code would, as though you had manually written it into the HTML document. Jinja2 can also use if and for statements, giving you immense control over the document you render. You can see this example in effect by examining lines 14-18 of home.html.
