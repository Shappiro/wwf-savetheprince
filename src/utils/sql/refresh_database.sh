#!/bin/bash
psql -U aaron -p 5432 -d prince -c 'REFRESH MATERIALIZED VIEW public.sitesummary;'
psql -U aaron -p 5432 -d prince -c 'UPDATE observations_site SET lunghezza=st_length(st_transform(geom,3035));'
