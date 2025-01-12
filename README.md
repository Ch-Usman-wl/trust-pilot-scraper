I have added two different ways to scrape trust pilot.

For the 2nd version you have to do a few things first.

Firstly, i recommend watching this video in order to understand how to get cookies/headers etc. https://www.youtube.com/watch?v=_wzFc_gPtV4

Next up, in the params which are inside while loop, add the businessUnit, it usually refers to the name of the company you are trying to scrape. Example:

'businessUnit': 'staytick.com'

Be sure to add url in the request.
