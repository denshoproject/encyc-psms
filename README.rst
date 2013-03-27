

[2012 apr 6 discussion]

- The repository holds the canonical metadata for various media objects (images, video, audio, documents, etc).

- The repository manages the actual files for some types of data (images, others?) but large files (video, audio?) would reside on Densho's streaming server; the repository would only ever link to video files.
Video metadata: pointers/signatures/checksums of the masters so that they can be located and validated.

- Each media object has one or more instances.  One of these instances is the master.

- Instance records can contain filesystem pointers, or possibly pointers to remote locations (URLs, DuraCloud, etc)


- Media object instances (except the master) may be cropped, downsized, or otherwise processed or munged.

- Media object instances have captions (or "description"s, to use Dublin Core).

- The encyclopedia has articles (duh).

- Encyclopedia articles can contain media, identified by Densho UID number.

- The media in encyclopedia articles are actually particular instances of media objects; articles do not point directly to media objects.

- Captions for media in encyclopedia articles comes from the particular media object instances.

- To phrase it another way, encyclopedia articles do not contain captions for media appearing on them.

- The repository and tansu make media objects available based on their Densho UIDs.

- Media object files in the repository and tansu contain the Densho UID.

- I suggest that instances of media object files should be identified by Densho UID plus an instance identifier.  Examples:
    denshopd-i35-00021-1
    denshovh-agene-01-0014-1

- Encyclopedia articles point to particular media objects using their Densho UID plus instance identifier.

- The encyclopedia should not know anything about tansu or the repository.

- Front should only know about tansu and the repository through an API.

- When encyclopedia pages are displayed to the public, media objects are displayed as thumbnails with captions and Javascript lightboxes.

- When displaying an encyclopedia page, Front will search for <a><img/></a> tags containing Densho UIDs-plus-instance-identifiers, query the tansu/repository API, and substitute or insert the caption and lightbox code.

- [Front will cache these pages so end-users don't have to wait for all of this every page-view.]

- [During editing, tansu/repository may upload image files to MediaWiki so media files used on encyclopedia article pages may be viewed in context.  Captions will not be visible on the page at this stage in the editing process].

- Links to media objects in encyclopedia articles will point to tansu until the repository is ready.

- Tansu and the repository will display media object instances as follows: the instance, its caption, a display thumbnail of the canonical media object, its metadata, and a link to download the actual media object.