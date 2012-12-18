var windowCount = 0;

function ClassHelper() {}
function ClassMain() {}
function ClassWindow() { this.id = ++windowCount; this.element = $('<div id="window' + this.id + '"></div>'); };
function ClassWindowRegister() {};

var Helper = new ClassHelper();
var Main = new ClassMain();

ClassHelper.prototype.getId = function(string) {
    var search = /(\d+)/;
    var result = search.exec(string);
    if ( result == null ) {
        return null;
    }
    return parseInt(result[1]);
}

ClassMain.prototype.load = function(element) {
    console.log(element.id);
};

ClassWindow.prototype.show = function(position,container = null) {
    if ( container != null ) {
        this.element.appendTo(container.element)
    } else {
        this.element.appendTo($('#container'));
        this.element.addClass('window');
    }
    
    
    if ( position != null ) {
        this.element.addClass(position);
    }
    if ( position == 'swap' ) {
        this.blind = $('<div id="windowswap' + this.id + '" class="blind">');
        $('<p>' + this.id + '</p>').appendTo(this.element);
        this.blind.appendTo(container.element);
        this.blind.click(this.swap);
        this.element.click(this.swap);
        
        this.element.hide();
    }
}

ClassWindow.prototype.swap = function(element) {
    var newStyle = 'width: ' + ( $(window).width() / 4 ) + 'px;';
    var id = Helper.getId(element.target.id);
    
    if ( id == null ) {
        return;
    }
    
    var windowIsTarget = false;
    if ( element.target.id == 'window' + id ) {
        var windowIsTarget = true;
    }
    
    if ( windowIsTarget ) {
        WindowRegister.get(id).blind.show();
        WindowRegister.get(id).element.hide();
    } else {
        WindowRegister.get(id).blind.hide();
        WindowRegister.get(id).element.show();
        WindowRegister.get(id).element.attr('style',newStyle);
    }
}

ClassWindowRegister.prototype.get = function(id) {
    return this.register[id];
}

ClassWindowRegister.prototype.newWindow = function() {
    var tmp = new ClassWindow();
    if ( this.register == null ) {
        this.register = new function() {};
    }
    this.register[tmp.id] = tmp;
    return tmp;
}

var WindowRegister = new ClassWindowRegister();