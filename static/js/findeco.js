var boxCount = 0;
var globalData;
var blablub;

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

ClassController.prototype.loadIndex = function(target) {
    Controller.position = target;
    document.location.hash = Controller.position;
}

ClassController.prototype.loadIndexRelative = function(target) {
    if ( Controller.position != '' ) {
        Controller.position += '/';
    }
    Controller.position = Controller.position + target;
    document.location.hash = Controller.position;
}

ClassController.prototype.position = '';

ClassController.prototype.stateHandler = function(event) {
    // TODO: Mockup legacy, remove or comment out after testing is done.
    if ( parseInt(document.location.hash.substring(1)) >= 0 || parseInt(document.location.hash.substring(1)) <= 100 ) {
        return;
    }
    if ( Controller.position != document.location.hash.substring(1) ) {
         Controller.position = document.location.hash.substring(1);
    }
    $.get('.json_loadIndex/' + Controller.position,function(json){
        loadCenterData(json);
    },'json');
    // console.log(event,event.originalEvent.state);
}

ClassData.prototype.load = function(data) {
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
    arguments['neutral']= $('<ul>')
        .addClass('argneutral')
        .appendTo(this.html);
    arguments['contra'] = $('<ul>')
        .addClass('argcontra')
        .appendTo(procontra);
    
    $('<br>').appendTo(procontra);
    
    for ( d in data ) {
        $('<li>' + data[d].fullTitle + '</li>').appendTo(arguments[data[d].shortTitle]);
    }
}

ClassData.prototype.loadIndexResponse = function(data) {
    this.type = 'index';
    
    for ( d in data ) {
        switch ( data[d].shortTitle ) {
            case 'pro': case 'neutral': case 'contra': this.loadArgumentResponse(data); return;
            default:
                $('<h2 data-shortTitle="' + data[d].shortTitle + '" data-index="' + data[d].index + '">' + data[d].fullTitle + '</h2>')
                    .appendTo(this.html)
                    .click(function () {
                        Controller.loadIndexRelative($(this).attr('data-shortTitle') + '.' + $(this).attr('data-index'));
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
    if ( element.id == 'content' ) {
        loadPosition();
    }
};

ClassBox.prototype.addButtons = function() {
    var arguments = this.element.children('div.arguments');
    var text = this.element.children('div.text');
    
    $('<div style="margin-bottom: 10px;">Zeige Argumente</div>')
        .addClass('button')
        .appendTo(arguments);
    $('<div style="margin-bottom: 10px;">Zeige Text</div>')
        .addClass('button')
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