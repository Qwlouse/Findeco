var boxCount = 0;
var globalData;

function ClassController() {}
function ClassData() {}
function ClassDataRegister() {this.register = new function() {};}
function ClassHelper() {}
function ClassMain() {}
function ClassBox() { this.id = ++boxCount; this.element = $('<div id="box' + this.id + '"></div>'); };
function ClassBoxRegister() {};

var Controller = new ClassController();
var DataRegister = new ClassDataRegister();
var Helper = new ClassHelper();
var Main = new ClassMain();
var BoxRegister = new ClassBoxRegister();

ClassController.prototype.load = function(target) {
    
}

/*
    {"loadIndexResponse":[{"shortTitle":"subtopic","index":1,"fullTitle":"This is a subtopic!","authorGroup":[{"test1"},{"test2"}]}]}
    
*/

ClassData.prototype.load = function(data) {
    this.html = $('<div>');
    this.html.addClass('innerContent');
    
    for ( d in data ) {
        if ( d == 'loadIndexResponse' ) {
            this.loadIndexResponse(data[d]);
        }
        if ( d == 'loadTextResponse' ) {
            this.loadTextResponse(data[d]);
        }
        if ( d == 'loadMicroBloggingResponse' ) {
            this.loadMicroBloggingResponse(data[d]);
        }
    }
};

ClassData.prototype.loadIndexResponse = function(data) {
    for ( d in data ) {
        $('<p>' + data[d].fullTitle + '</p>').appendTo(this.html);
    }
};

ClassData.prototype.loadTextResponse = function(data) {
    for ( p in data['paragraphs'] ) {
        $('<p>' + data['paragraphs'][p].wikiText + '</p>').appendTo(this.html);
    }
};

ClassData.prototype.loadMicroBloggingResponse = function(data) {
    for ( p in data ) {
        var author = '';
        for ( a in data[p].authorGroup ) {
            if ( author != '' ) {
                author = author + ',';
            }
            author = author + data[p].authorGroup[a].displayName;
        }
        var div = $('<div>')
            .addClass("microBlogPost")
            .appendTo(this.html);
        $('<p>' + author + ':&nbsp;' + data[p].microBlogText + '</p>')
            .appendTo(div);
        $('<p>' + Helper.timestampToDate(data[p].microBlogTime) + ' (' + data[p].microBlogID + ')</p>')
            .addClass("time")
            .appendTo(div);
    }
};

ClassData.prototype.getJQueryObject = function() {
    return this.html;
}

ClassHelper.prototype.getId = function(string) {
    var search = /(\d+)/;
    var result = search.exec(string);
    if ( result == null ) {
        return null;
    }
    return parseInt(result[1]);
}

ClassHelper.prototype.timestampToDate = function(time) {
    var d = new Date();
    d.setTime(time*1000);
    return d.toLocaleTimeString() + ', ' + d.toLocaleDateString(); 
}

ClassMain.prototype.load = function(element) {
    if ( element.id == 'imprint' ) {
        loadImprint();
    }
};

ClassBox.prototype.printData = function(data,append = null) {
    if ( append == null ) {
        this.element.empty();
    }
    this.element.append(data.getJQueryObject());
}

ClassBox.prototype.empty = function() {
    this.element.empty();
}

ClassBox.prototype.show = function(position,container) {
    if ( container != null ) {
        this.element.appendTo(container.element)
    } else {
        this.element.appendTo($('#container'));
        this.element.addClass('box');
    }
    
    
    if ( position != null ) {
        this.element.addClass(position);
    }
    if ( position == 'swap' ) {
        $('<p>' + this.id + '</p>').appendTo(this.element);
        this.blind = $('<div id="boxswap' + this.id + '" class="blind">');
        this.blind.appendTo(container.element);
        this.blind.click(this.swap);
        this.element.click(this.swap);
        
        this.element.hide();
    }
}

ClassBox.prototype.swap = function(element) {
    var id = Helper.getId(element.target.id);
    
    if ( id == null ) {
        return;
    }
    
    var boxIsTarget = false;
    if ( element.target.id == 'box' + id ) {
        var boxIsTarget = true;
    }
    
    if ( boxIsTarget ) {
        BoxRegister.get(id).blind.show();
        BoxRegister.get(id).element.hide();
    } else {
        BoxRegister.hideAll();
        BoxRegister.get(id).blind.hide();
        BoxRegister.get(id).element.show();
        var newStyle = 'width: ' + ( $(window).width() / 4 ) + 'px;';
        BoxRegister.get(id).element.attr('style',newStyle);
    }
}

ClassBoxRegister.prototype.get = function(id) {
    return this.register[id];
}

ClassBoxRegister.prototype.hideAll = function() {
    for ( r in this.register ) {
        if ( this.register[r].blind == undefined 
            || this.register[r].element == undefined ) {
            continue;
        }
        this.register[r].blind.show();
        this.register[r].element.hide();
    }
}

ClassBoxRegister.prototype.newBox = function() {
    var tmp = new ClassBox();
    if ( this.register == null ) {
        this.register = new function() {};
    }
    this.register[tmp.id] = tmp;
    return tmp;
}