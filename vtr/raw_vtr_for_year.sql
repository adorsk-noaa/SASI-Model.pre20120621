SELECT
t.tripid,
t.tripcatg,  
t.datesail,
t.timesail,
t.datelnd1 datelnd1, 
t.permit permit, 
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
a.nespp4,
v.vp_num, 
v.hport,
v.hpst,
v.pport,
v.ppst,
v.ap_year,
v.ves_name,
v.gtons,
v.vhp,
v.len

FROM
VESLOG{{YEAR}}T t LEFT JOIN VESLOG{{YEAR}}G g ON t.tripid = g.tripid
LEFT JOIN VESLOG{{YEAR}}S s ON s.tripid = t.tripid AND s.gearid = g.gearid
LEFT JOIN VLSPPTBL a on s.sppcode = a.sppcode
LEFT JOIN VPS_VESSEL v ON t.permit = v.vp_num
WHERE
t.tripcatg in (1, 4)
AND v.ap_year = {{YEAR}}
;
