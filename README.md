a3-plvines-djpeter  
===============

## Team Members

1. Paul Vines plvines@cs.washington.edu
2. Peter Henry peter@cs.washington.edu

## Visualization of Artist Similarities from the Million Song Dataset
Shows the selected artist and related artists,
"sorted" by decade, with the artist placed at the center of their
career's timeline and lines stretching out to indicate when they
started and stopped making music.
Hovering over an artist displays a tooltip with a few details and a
list of songs, one per year they released an album. These songs are
links to youtube queries, so clicking on one should take you to a list
of youtube videos containing the song.
Finally, we allow the user to sort the similar artists vertically by
either familiarity or hotttnesss, both scores calculated by the
dataset creators.

## Running Instructions

Access our visualization at http://patillo.cs.washington.edu/~cse512

You may also download this repository and run our code, however it requires some large database files. These can be obtained by visiting http://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset and downloading the three SQLite files and placing them in cgi-bin/sqlite/ in the repository.


## Story Board

[link to our storyboard pdf file](storyboard.pdf?raw=true) here.  
The idea here is to let the user browse for artists similar to artists
they already like, but potentially in different decades. 
This would both allow for a nifty visualization of music history (such
as seeing clusters of bands of a certain type coming in in a wave) and
useful exploration of bands a viewer might be interested in trying.
Along these lines, we wanted a simple way to pivot the search to allow
the user to go through a chain of artists, looking at similar artists
for each one, without doing much work. So, just by clicking on an
artist they can pivot the search to focus on this new artist.
We also wanted to give the user an easy way to listen to the artists
they found, so some kind of link-to-music would be handy.
The idea was to start with one artist and then step away from that
artist along the similarity graph, showing each link with a line
between the source artist and the similarity.


### Changes between Storyboard and the Final Implementation
The original storyboard did not include the career span of the
artists. We thought this would be a more interesting view, and allow
users to better understand the data and get a better feel for which
bands were really long lasting and which were only 1 (or a few) hit
wonders. 
Additionally, we discarded the idea of lines linking the artists, both
to allow showing the date range with lines and to avoid the clutter
that it would introduce. Furthermore, because of the large number of
similar artists contained by the dataset, it became unnecessary to do
multiple steps along the similarity graph, an so the lines would have
just been one line between each artist and the selected artist, which
would have been pointless.
We also removed the ability to select decades to view. For one reason,
the graph was clear enough even with all decades shown all the time
and the X axis was not the limiting factor in the
visualization.



## Development Process
{Paul} I wrote all of the visualization front-end from sending the
queries to the python back-end to drawing the D3/SVG objects and user
interface buttons. I also produced the storyboard. I would say I
worked approximately 28 hours on this assignment. I would say
development was about equal. Trying to make D3 separate data and draw it correctly was the most difficult, particularly time spend trying to make it draw lines between elements. Also, trying to make the tooltips sticky.


{Peter} I configured a machine to serve database query results as JSON
objects to the front-end.  This involved modifying the apache
configuration on my machine, writing Python CGI code to pass URL
parameters to Python functions, and wrapping custom SQL queries to the SQLite database
files which were downloaded from the Million Song Dataset website. I
would agree that we contributed equally to this project.  Configuring
Apache and getting a handle on Python and JSON was a bit trickier than
I would have guessed.
