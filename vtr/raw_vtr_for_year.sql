SELECT
t.tripid,
t.tripcatg,  
t.datesail,
t.timesail,
t.datelnd1 datelnd1, 
t.hullnum,
t.port, 
t.crew,
g.gearid,
g.gearcode gear,
g.mesh,
g.gearqty,
g.gearsize,
g.nhaul,
g.soakhrs,
g.soakmin,
g.depth,
g.clatdeg,
g.clatmin,
g.clatsec,
g.clondeg,
g.clonmin,
g.clonsec,
g.qdsq,
g.cnemarea nemarea,
g.tenmsq, 
s.sppcode,
s.tripid,
s.qtykept keptlb,
s.qtydisc disclb,
s.datesold, 
s.dealnum,
a.nespp4

FROM
VESLOG{{YEAR}}T t,
VESLOG{{YEAR}}G g, 
VESLOG{{YEAR}}S s LEFT JOIN VLSPPTBL a ON s.sppcode = a.sppcode

WHERE
s.tripid=t.tripid
and s.tripid=g.tripid
and s.gearid=g.gearid 
and t.tripcatg in (1, 4)
