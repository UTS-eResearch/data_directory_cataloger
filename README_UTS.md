# README for UTS

For the UTS setup of the Data Directory Cataloger there are several files that
are not checked into this repository.

The following files can be found under the "uts_backups" directory.

The configuration files for the MkDocs environments for the various groups:

    mkdocs_aimi.yml
    mkdocs_crg.yml
    mkdocs_c3.yml
    mkdocs_eresearch.yml
    mkdocs_rsg.yml

The home pages for the MkDocs environments for the groups:

    index_aimi.md
    index_c3.md
    index_crg.md
    index_eresearch.md
    index_rsg.md

These scripts are in the `bin` directory:

    update_common.sh            Updates CSS, image files, about and index 
                                files for all sites.
    update_site_aimi.sh         Updates the site.
    update_site_c3.sh           ...
    update_site_crg.sh          ...
    update_site_eresearch.sh    ...
    update_site_rsg.sh          ...

These files are the same for all sites and are in the `common` directory:

    about_template.md
    howto.md
    other.md
    css/extra.css
    images/uts_logo.png

Mike Lake
January 2023

