

db.system.js.save(
    {
        _id : "get_drivers" ,
        value : function (x, y, maxdist, drivers_amount)
        {return db.runCommand({
            geoNear: "driver",
            near: { type: "Point", coordinates: [x,y]},
            spherical: true,
            query: { is_free: 1 },
            maxDistance: maxdist,
            num: drivers_amount
            //query: db.driver.find( { is_free: 1} )

        })}

   }
);
   
   
db.loadServerScripts();
   
   
   
get_drivers(-0.148004, 51.516894,3500,100)