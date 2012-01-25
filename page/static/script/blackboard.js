if(!window.Awesome) { var Awesome = {}; }
if(!Awesome.plugins) { Awesome.plugins = {}; }

(function() {
    
    Awesome.plugins.Blackboard = Class.create({
       
       initialize: function(attr) {       
           var that = this;
           
           $(document).observe("dom:loaded", function() {
               that.handleLoad(attr.date);
               
               if(attr.position === "center") {
                   that.centerHorizontally()
               }
           });
       },
       
       handleLoad: function(date) {
           this.dom = $("blackboard");
           this.dom.setStyle({
               backgroundImage: "url(" + Awesome.const.STATIC + "/images/events/" + date + ".png)"
           });
       },
       
       moveTo: function(x, y) {
           this.dom.setStyle({
               marginLeft: x + "px",
               marginTop: y + "px"
           });
       },
       
       centerHorizontally: function() {
           var viewport = document.viewport;
           
           this.moveTo((viewport.getWidth() / 2) - (this.dom.getWidth() / 2), 0);
       }
        
    });
    
}());