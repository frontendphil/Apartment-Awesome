if(!window.Awesome) { var Awesome = {}; }
if(!Awesome.plugins) { Awesome.plugins = {}; }

(function() {
    
    Awesome.plugins.Blackboard = Class.create({
       
       initialize: function(attr) {       
           var that = this;
           
           $(document).observe("dom:loaded", function() {
               that.handleLoad(attr.date);
           });
       },
       
       handleLoad: function(date) {
           this.dom = $("blackboard");
           this.dom.setStyle({
               backgroundImage: "url(" + Awesome.const.STATIC + "/images/events/" + date + ".png)"
           });
       }
        
    });
    
}());