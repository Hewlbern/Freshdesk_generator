-- SQLite
-- SQLite
-- open FreshCodes.sqlite3;
-- SELECT * FROM activities_data;


-- /*Time spent Open - So the current time minus the ticket open time; if it has been closed, final ticket time minus original time (Excluding this for speed).*/

SELECT ( ( end_at - start_at ) / 1000 / 60 / 60 ) 
FROM metadata ;
-- -- time spent waiting on customer

SELECT ( ( performed_at - shipping_date ) / 1000 / 60 / 60 )

FROM activities_data

WHERE status = 'closed';

-- Time spent waiting for response (Pending Status)

SELECT ( ( performed_at - shipping_date ) / 1000 / 60 / 60 )

FROM activities_data

WHERE status = 'pending';

-- Time till resolution - time to solved.
SELECT ( ( performed_at - shipping_date ) / 1000 / 60 / 60 )

FROM activities_data

WHERE status = 'resolved';

-- Time to first response (First time to first ticket time).
SELECT ( ( performed_at - shipping_date ) / 1000 / 60 / 60 )

FROM activities_data

WHERE status = 'resolved'OR'pending'OR'closed'OR'waiting for customer'OR'waiting for third party'OR'open';