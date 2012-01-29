if(!window.Awesome) { var Awesome = {}; }
if(!Awesome.utils) { Awesome.utils = {}; }

(function() {
    
    Awesome.utils.Linker = {
        register: function(attr) {
            var register = function(a) {
                $(a.id).observe("click", function() {
                    window.location.href = a.href;
                });
            };
            
            if(attr instanceof Array) {
                attr.each(register);
            } else {
                register(attr);
            }
        }
    }
    
}());