var boxCount = 0;
var globalData;
var blablub;

function ClassBox() { this.id = ++boxCount; this.element = $('<div id="box' + this.id + '"></div>'); };
function ClassBoxRegister() {};
function ClassController() {}
function ClassData(json) {this.load(json);}
function ClassDataRegister() {this.register = new function() {};}
function ClassHelper() {}
function ClassMain() {}
function ClassMicroblogging() {}
function ClassNavigation() {}

var BoxRegister = new ClassBoxRegister();
var Controller = new ClassController();
var DataRegister = new ClassDataRegister();
var Helper = new ClassHelper();
var Main = new ClassMain();
var Microblogging = new ClassMicroblogging();
var Navigation = new ClassNavigation();

ClassBox.prototype.addButtons = function() {
    var arguments = this.element.children('div.arguments');
    var text = this.element.children('div.text');
    
    $('<div style="margin-bottom: 10px;">Zeige Argumente</div>')
        .addClass('button')
        .click(function () {
            Controller.loadArguments();
        })
        .appendTo(arguments);
    $('<div style="margin-bottom: 10px;">Zeige Text</div>')
        .addClass('button')
        .click(function () {
            Controller.loadText();
        })
        .appendTo(text);
}

ClassBox.prototype.printData = function(data) {
    var target = this.element;
    switch ( data.getType() ) {
        case 'index':
            target = this.element.children('div.indizes');
        break;
        case 'text':
            target = this.element.children('div.text');
        break;
        case 'argument':
            target = this.element.children('div.arguments');
        break;
    }
    
    if ( this.element.parent().hasClass('left') ) {
        var target = this.element;
    }
    target.empty();
    
    data.getJQueryObject().appendTo(target);
}

ClassBox.prototype.empty = function() {
    if ( this.type == 'center' ) {
        this.element.children().empty();
        this.addButtons();
    } else {
        this.element.empty();
    }
}

ClassBox.prototype.show = function(position,container) {
    this.type = position;
    if ( container != null ) {
        this.element.appendTo(container.element)
    } else {
        this.element.appendTo($('#container'));
        this.element.addClass('box');
    }
    
    if ( position != null ) {
        this.element.addClass(position);
    }
    
    if ( position == 'center' ) {
        $('<div>')
            .addClass('indizes')
            .appendTo(this.element);
        $('<div>')
            .addClass('arguments')
            .appendTo(this.element);
        $('<div>')
            .addClass('text')
            .appendTo(this.element);
        
        this.addButtons();
        
        // console.log(this.element,this.element.children());
    } else if ( position == 'swap' ) {
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

ClassController.prototype.load = function(element) {
    if ( element.id == 'imprint' ) {
        loadImprint();
    }
    if ( element.id == 'content' ) {
        loadPosition();
    }
};

ClassController.prototype.loadArguments = function() {
    Main.loadArguments(Controller.position);
}
ClassController.prototype.loadText = function() {
    Main.loadText(Controller.position);
}

ClassController.prototype.loadIndex = function(target) {
    Controller.position = target;
    document.location.hash = Controller.position;
}

ClassController.prototype.loadIndexRelative = function(target) {
    if ( Controller.position.substring(Controller.position.length-1) != '/' ) {
        Controller.position += '/';
    }
    Controller.position += target;
    document.location.hash = Controller.position;
}

ClassController.prototype.parentPosition = function() {
    var pos = Controller.position.lastIndexOf('/');
    if ( pos == -1 ) {
        return Controller.position;
    }
    return Controller.position.substring(0,pos + 1);
};

ClassController.prototype.position = '/';

ClassController.prototype.stateHandler = function(event) {
    // TODO: Mockup legacy, remove or comment out after testing is done.
    if ( parseInt(document.location.hash.substring(1)) >= 0 || parseInt(document.location.hash.substring(1)) <= 100 ) {
        return;
    }
    
    if ( Controller.position != document.location.hash.substring(1) ) {
         Controller.position = document.location.hash.substring(1);
    }
    // console.log('ClassController','stateHandler',event,document.location.hash);
    Microblogging.load(Controller.position);
    Navigation.load(Controller.position);
    Main.load(Controller.position);
}

ClassData.prototype.load = function(data) {
    this.json = data;
    
    this.html = $('<div>');
    this.html.addClass('innerContent');
    
    // console.log(data);
    
    for ( d in data ) {
        if ( d == 'loadIndexResponse' ) {
            this.loadIndexResponse(data[d]);
        }
        if ( d == 'loadTextResponse' ) {
            this.loadTextResponse(data[d]);
        }
        if ( d == 'loadMicrobloggingResponse' ) {
            this.loadMicrobloggingResponse(data[d]);
        }
    }
};

ClassData.prototype.loadArgumentResponse = function(data) {
    this.type = 'argument';
    
    var procontra = $('<div>')
        .addClass('argprocontra')
        .appendTo(this.html);
    var arguments = {};
    arguments['pro'] = $('<ul>')
        .addClass('argpro')
        .appendTo(procontra);
    arguments['neut']= $('<ul>')
        .addClass('argneutral')
        .appendTo(this.html);
    arguments['con'] = $('<ul>')
        .addClass('argcontra')
        .appendTo(procontra);
    
    $('<br>').appendTo(procontra);
    
    for ( d in data ) {
        console.log(data[d]);
        $('<li>' + data[d].fullTitle + '</li>').appendTo(arguments[data[d].shortTitle]);
    }
}

ClassData.prototype.loadIndexResponse = function(data) {
    this.type = 'index';
    
    parent = '';
    if ( typeof this.info == 'object' && this.info.path != undefined ) {
        parent = 'data-parent="' + this.info.path + '"';
    }
    
    for ( d in data ) {
        switch ( data[d].shortTitle ) {
            case 'pro': case 'neut': case 'con': this.loadArgumentResponse(data); return;
            default:
                if ( parent != '' ) {
                    var parentpath = this.info.path;
                    if ( parentpath.substring(parentpath.length-1) != '/' ) {
                        parentpath += '/';
                    }
                    DataRegister.setTitle(parentpath + data[d].shortTitle + '.' + data[d].index,data[d].fullTitle);
                }
                $('<h2 data-shortTitle="' + data[d].shortTitle + '" data-index="' + data[d].index + '"' + parent + '>' + data[d].fullTitle + '</h2>')
                    .appendTo(this.html)
                    .click(function () {
                        if ( $(this).attr('data-parent') == undefined ) {
                            Controller.loadIndexRelative($(this).attr('data-shortTitle') + '.' + $(this).attr('data-index'));
                        } else {
                            var parent = $(this).attr('data-parent');
                            if ( parent.substring(parent.length-1) != '/' ) {
                                parent += '/';
                            }
                            Controller.loadIndex(parent + $(this).attr('data-shortTitle') + '.' + $(this).attr('data-index'));
                        }
                    });
        }
    }
};

ClassData.prototype.loadTextResponse = function(data) {
    this.type = 'text';
    
    for ( p in data['paragraphs'] ) {
        $('<p>' + data['paragraphs'][p].wikiText + '</p>').appendTo(this.html);
    }
};

ClassData.prototype.loadMicrobloggingResponse = function(data) {
    for ( p in data ) {
        var author = '';
        for ( a in data[p].authorGroup ) {
            if ( author != '' ) {
                author = author + ',';
            }
            author = author + data[p].authorGroup[a].displayName;
        }
        var div = $('<div>')
            .addClass("microblogPost")
            .appendTo(this.html);
        $('<p>' + author + ':&nbsp;' + data[p].microblogText + '</p>')
            .appendTo(div);
        $('<p>' + Helper.timestampToDate(data[p].microblogTime) + ' (' + data[p].microblogID + ')</p>')
            .addClass("time")
            .appendTo(div);
    }
};

ClassData.prototype.getJQueryObject = function() {
    return this.html;
}

ClassData.prototype.getType = function() {
    return this.type;
}

ClassData.prototype.setInfo = function(type,path) {
    this.info = {'type':type,'path':path};
}

ClassData.prototype.getInfo = function() {
    return this.info;
}

ClassDataRegister.prototype.data = {'index':{},'text':{},'microblogging':{},'argument':{}};

ClassDataRegister.prototype.get = function(callback,type,position,force) {
    // console.log('ClassDataRegister','get',force);
    if ( DataRegister.data[type][position] == undefined
        || force != undefined ) {
        DataRegister.load(callback,type,position);
        return;
    }
    var data = new ClassData();
    data.setInfo(type,position);
    data.load(DataRegister.data[type][position]);
    callback(data);
}

ClassDataRegister.prototype.getTitle = function(path) {
    return this.title[path];
}

ClassDataRegister.prototype.handleAjax = function(json) {
    var action = Helper.getActionFromUrl(this.url);
    var position = Helper.getTargetPathFromUrl(this.url);
    
    var type = '';
    
    switch ( action ) {
        case '.json_loadIndex': 
            type = 'index';
            if ( position.substring(0,5) == '/True' ) {
                type = 'argument';
                position = position.substring(5);
            }
        break;
        case '.json_loadMicroblogging':
            type = 'microblogging'; 
            position = position.replace(/\/(newer|older)/g,'');
            position = position.replace(/\/\d+/g,'');
        break;
        case '.json_loadText': type = 'text'; break;
    }
    // console.log(type,position,DataRegister.data[type]);
    var callbacks = DataRegister.data[type][position];
    
    DataRegister.data[type][position] = json;
    
    var data = new ClassData();
    data.setInfo(type,position);
    data.load(DataRegister.data[type][position]);
    
    // console.log(data,callbacks);
    
    for ( c in callbacks ) {
        if ( c == 'next' ) {
            continue;
        }
        // console.log(callbacks,c);
        callbacks[c](data);
    }
    
    // Necessary call to ensure that Navigation Buttons are allways filled!
    Navigation.updateButtons();
}

ClassDataRegister.prototype.load = function(callback,type,position) {
    // console.log('ClassDataRegister','load');
    // Storing the callback reference into the data object for future reference.
    if ( typeof DataRegister.data[type][position] != 'object' 
        || DataRegister.data[type][position].next == undefined ) {
        DataRegister.data[type][position] = {'next':1,0:callback};
    } else {
        DataRegister.data[type][position][DataRegister.data[type][position].next++] = callback;
        return;
    }
    
    var loadType = '';
    
    switch ( type ) {
        case 'index': loadType = '.json_loadIndex'; break;
        case 'microblogging': $.get('.json_loadMicroblogging/newer' + position,DataRegister.handleAjax,'json'); return;
        case 'argument': $.get('.json_loadIndex/True' + position,DataRegister.handleAjax,'json'); return;
        case 'text': loadType = '.json_loadText'; break;
    }
    
    $.get(loadType + position,DataRegister.handleAjax,'json');
}

ClassDataRegister.prototype.setTitle = function(path,title) {
    this.title[path] = title;
}

ClassDataRegister.prototype.title = {};

ClassHelper.prototype.getActionFromUrl = function(url) {
    return url.substring(0,url.indexOf('/'));
}

ClassHelper.prototype.getId = function(string) {
    var search = /(\d+)/;
    var result = search.exec(string);
    if ( result == null ) {
        return null;
    }
    return parseInt(result[1]);
}

ClassHelper.prototype.getTargetPathFromUrl = function(url) {
    return url.substring(url.indexOf('/'));
}

ClassHelper.prototype.objectLength = function(object) {
    var i = 0;
    for ( o in object ) {
        i++;
    }
    return i;
}

ClassHelper.prototype.timestampToDate = function(time) {
    var d = new Date();
    d.setTime(time*1000);
    return d.toLocaleTimeString() + ', ' + d.toLocaleDateString(); 
}

ClassMain.prototype.load = function (position) {
    // console.log('ClassMain','load');
    DataRegister.get(this.show,'index',position,true);
};

ClassMain.prototype.loadArguments = function (position) {
    // console.log('ClassMain','loadArguments');
    DataRegister.get(Main.append,'argument',position,true);
};

ClassMain.prototype.loadText = function (position) {
    // console.log('ClassMain','loadText');
    DataRegister.get(Main.append,'text',position,true);
};

ClassMain.prototype.show = function (data) {
    // console.log('ClassMain','show');
    center.empty();
    Main.append(data);
}

ClassMain.prototype.append = function (data) {
    // console.log('ClassMain','append');
    if ( data.json.loadIndexResponse != undefined 
        && Helper.objectLength(data.json.loadIndexResponse) == 0 ) {
        Controller.loadText();
    } else {
        center.printData(data);
    }
};

ClassMicroblogging.prototype.load = function (position) {
    // console.log('ClassMicroblogging','load');
    DataRegister.get(this.show,'microblogging',position,true);
};

ClassMicroblogging.prototype.show = function (data) {
    // console.log('ClassMicroblogging','show');
    right.empty();
    right.printData(data);
};

ClassNavigation.prototype.load = function (position) {
    left.empty();
    navigation.empty();
    
    if ( position == '/' ) {        
        return;
    }
    
    var tmp = position.split('/');
    Navigation.elements = {'boxes':{},'buttons':{}};
    
    var path = '';
    for ( var i = 0 ; i < tmp.length ; i++ ) {
        if ( path.substring(path.length-1) != '/' ) {
            path += '/';
        }
        path += tmp[i];
        if ( i < tmp.length - 1 ) {
            Navigation.elements['boxes'][path] = BoxRegister.newBox();
            Navigation.elements['boxes'][path].show('swap',left);
        
            DataRegister.get(Navigation.show,'index',path);
        }
        if ( i > 0 ) {
            $('<li class="button" style="z-index: 501; position: relative;" data-path="' + path + '"></li>')
                .click(function() {
                    var path = $(this).attr('data-path');
                    Controller.loadIndex(path);
                })
                .appendTo(navigation);
        }
    }
};

ClassNavigation.prototype.show = function (data) {
    // console.log('ClassNavigation','show');
    var info = data.getInfo();
    Navigation.elements['boxes'][info['path']].printData(data);
};

ClassNavigation.prototype.updateButtons = function () {
    // console.log('ClassNavigation','updateButtons');
    var buttons = navigation.children();
    for ( b in buttons ) {
        if ( isNaN(b) ) {
            continue;
        }
        var path = buttons[b].getAttribute('data-path');
        var title = DataRegister.getTitle(path);
        if ( title == undefined ) {
            continue;
        }
        buttons[b].innerHTML = title;
    }
}