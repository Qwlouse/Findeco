/** It's all Svens fault!!1!11 **********************************************************
 * Copyright (c) 2012 Justus Wingert <justus_wingert@web.de>                            *
 *                                                                                      *
 * This file is part of Findeco.                                                        *
 *                                                                                      *
 * Findeco is free software; you can redistribute it and/or modify it under             *
 * the terms of the GNU General Public License as published by the Free Software        *
 * Foundation; either version 3 of the License, or (at your option) any later           *
 * version.                                                                             *
 *                                                                                      *
 * Findeco is distributed in the hope that it will be useful, but WITHOUT ANY           *
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A      *
 * PARTICULAR PURPOSE. See the GNU General Public License for more details.             *
 *                                                                                      *
 * You should have received a copy of the GNU General Public License along with         *
 * Findeco. If not, see <http://www.gnu.org/licenses/>.                                 *
 ****************************************************************************************/
 
/****************************************************************************************
 * This Source Code Form is subject to the terms of the Mozilla Public                  *
 * License, v. 2.0. If a copy of the MPL was not distributed with this                  *
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.                             *
 ****************************************************************************************/

 /*
 * Workaround for JQueryObject.val() destroying carriage returns.
 */
 
$.valHooks.textarea = {
	get: function( elem ) {
		return elem.value.replace( /\r?\n/g, "\r\n" );
	} 

};
 
function ClassContribute() {
	this.temp={};
}


	

ClassContribute.prototype.close = function () {
    if ( $(this).attr('id') == 'overlay' || $(this).attr('id') == 'cancelbutton' ) {
        if ( Contribute.isDefaultText(Contribute.form['wikiText'].val()) != true ) {
            if ( confirm('Wollen sie wirklich das Formular verlassen? Nicht gespeicherte Zwischenstände gehen so verloren.') ) {
                $('#overlay').hide();
            }
            return false;
        }
        $('#overlay').hide();
    }
}

ClassContribute.prototype.isDefaultText = function (text) {
    if ( text == '' ) {
        return true;
    }
    for ( d in Contribute.defaultText ) {
        for ( d2 in Contribute.defaultText[d] ) {
            if ( Contribute.defaultText[d][d2] == text ) {
                return true;
            }
        }
    }
    return false;
}

ClassContribute.prototype.generateButtons= function(){
	 // Generate Dropdown menues for new content Creation
	
    DropdownText =$('<div style=" margin: 0 auto; width: 280px;"><div class="btndropdown" style=" width: 135px;"><ul> <li> Textoptionen<img src="static/images/dropdown.png" alt="S" title="Sp"> <ul></ul></li></ul></div></div>');
    DropdownArguments =$('<div style=" margin: 0 auto; width: 280px;"><div class="btndropdown" style=" width: 135px;"><ul><li> Argumente<img src="static/images/dropdown.png" alt="S" title="Sp"> <ul></ul></li></ul></div></div><div style="clear:both"></div>');
    
    DropdownText.find(".btndropdown li:has(ul)").hover(function(){
		$(this).find("ul").slideDown();
	}, function(){
		$(this).find("ul").hide();
	});

    DropdownArguments.find(".btndropdown li:has(ul)").hover(function(){
		$(this).find("ul").slideDown();
	}, function(){
		$(this).find("ul").hide();
	});
    
    
   
    $('<li><div>Pro Argument</div></li>')
    	.click(Contribute.setViewNewPro)
    	.appendTo(DropdownArguments.find("ul ul"));
    $('<li><div>Contra Argument</div></li>')
    	.click(Contribute.setViewNewCon)
    	.appendTo(DropdownArguments.find("ul ul"));
    $('<li><div>Neutrales Argument</div></li>')
    	.click(Contribute.setViewNewNeut)
    	.appendTo(DropdownArguments.find("ul ul"));
    
    
    $('<li><div>Neuer Abschnitt</div></li>')
    	.click(Contribute.setViewNewSection )
    	.appendTo(DropdownText.find("ul ul"));
    $('<li><div>Neue Alternative</div></li>')
    	.click(Contribute.setViewAlternativeText )
    	.appendTo(DropdownText.find("ul ul"));
    $('<li><div>Weiterentwickeln</div></li>')
    	.click(Contribute.setViewDerivateText )
    	.appendTo(DropdownText.find("ul ul"));
   return DropdownText.add(DropdownArguments);    
}

ClassContribute.prototype.defaultText = {
    'text': {
        'wikiText':'= Ersetze dies hier durch einen Titel für deinen Text =' + "\r\n" 
                    + 'Der Titel wird in der Übersicht angezeigt. Dieser Text hier unten ist erst sichtbar wenn jemand auf den verlinkten Titel geklickt hat!' + "\r\n"  + "\r\n" 
                    + 'Der eingegebene Text wird automatisch umgewandelt, du siehst also sofort ob deine Formatierung stimmt!'
    },
    'arg': {
        'wikiText':'= Ersetze dies hier durch einen Titel oder eine Kurzbeschreibung für dein Argument =' + "\r\n" 
                    + 'Der Titel beziehungsweise die Kurzbeschreibung ist in der Übersicht der Argumente sichtbar. Dieser Text hier unten ist erst sichtbar wenn jemand auf den verlinkten Titel geklickt hat!' + "\r\n"  + "\r\n" 
                    + 'Der eingegebene Text wird automatisch umgewandelt, du siehst also sofort ob deine Formatierung stimmt!'
    },
    'alternative': {
        'wikiText':'= Ersetze dies hier durch einen Titel oder eine Kurzbeschreibung deines Arguments für einen Alternativtext =' + "\r\n" 
                    + 'Der Titel beziehungsweise die Kurzbeschreibung ist in der Übersicht der Argumente sichtbar. Dieser Text hier unten ist erst sichtbar wenn jemand auf den verlinkten Titel geklickt hat!' + "\r\n"  + "\r\n" 
                    + 'Der eingegebene Text wird automatisch umgewandelt, du siehst also sofort ob deine Formatierung stimmt!'
    },
    'derivate': {
        'wikiText':'= Ersetze dies hier durch den Titel deiner Weiterentwicklung =' + "\r\n" 
                    + 'Der Titel beziehungsweise die Kurzbeschreibung ist in der Übersicht der Argumente sichtbar. Dieser Text hier unten ist erst sichtbar wenn jemand auf den verlinkten Titel geklickt hat!' + "\r\n"  + "\r\n" 
                    + 'Der eingegebene Text wird automatisch umgewandelt, du siehst also sofort ob deine Formatierung stimmt!',
        'wikiTextReason':'= Ersetze dies hier durch eine Begründung für deine Weiterentwicklung =' + "\r\n" 
                    + 'Der Titel beziehungsweise die Kurzbeschreibung ist in der Übersicht der Argumente sichtbar. Dieser Text hier unten ist erst sichtbar wenn jemand auf den verlinkten Titel geklickt hat!' + "\r\n"  + "\r\n" 
                    + 'Der eingegebene Text wird automatisch umgewandelt, du siehst also sofort ob deine Formatierung stimmt!'
    },
    'pro': {
        'wikiText':'= Ersetze dies hier durch einen Titel oder eine Kurzbeschreibung deines Arguments für einen Alternativtext =' + "\r\n" 
                    + 'Der Titel beziehungsweise die Kurzbeschreibung ist in der Übersicht der Argumente sichtbar. Dieser Text hier unten ist erst sichtbar wenn jemand auf den verlinkten Titel geklickt hat!' + "\r\n"  + "\r\n" 
                    + 'Der eingegebene Text wird automatisch umgewandelt, du siehst also sofort ob deine Formatierung stimmt!'
    },
    'con': {
        'wikiText':'= Ersetze dies hier durch einen Titel oder eine Kurzbeschreibung deines Arguments für einen Alternativtext =' + "\r\n" 
                    + 'Der Titel beziehungsweise die Kurzbeschreibung ist in der Übersicht der Argumente sichtbar. Dieser Text hier unten ist erst sichtbar wenn jemand auf den verlinkten Titel geklickt hat!' + "\r\n"  + "\r\n" 
                    + 'Der eingegebene Text wird automatisch umgewandelt, du siehst also sofort ob deine Formatierung stimmt!'
    },
    'neut': {
        'wikiText':'= Ersetze dies hier durch einen Titel oder eine Kurzbeschreibung deines Arguments für einen Alternativtext =' + "\r\n" 
                    + 'Der Titel beziehungsweise die Kurzbeschreibung ist in der Übersicht der Argumente sichtbar. Dieser Text hier unten ist erst sichtbar wenn jemand auf den verlinkten Titel geklickt hat!' + "\r\n"  + "\r\n" 
                    + 'Der eingegebene Text wird automatisch umgewandelt, du siehst also sofort ob deine Formatierung stimmt!'
    }
};

ClassContribute.prototype.checkDone = function () {
    switch ( Contribute.formType ) {
        case 'pro':case 'neut':case 'con':
            Contribute.buttons['confirm'].removeClass('marked');
            if ( Contribute.isDefaultText(Contribute.form['wikiText'].val()) ) {
                Contribute.buttons['confirm'].addClass('marked');
                return false;
            }
            Parser.parse(Contribute.form['wikiText'].val());
            if ( Parser.errorState == true ) {
                return false;
            }
        return true;
        case 'text':
            Contribute.buttons['confirm'].removeClass('marked');
            if ( Contribute.isDefaultText(Contribute.form['wikiText'].val()) ) {
                Contribute.buttons['confirm'].addClass('marked');
                return false;
            }
            Parser.parse(Contribute.form['wikiText'].val());
            if ( Parser.errorState == true ) {
                console.log('wikiText');
                return false;
            }
        return true;
        case 'alternative':
        	
            Contribute.buttons['confirm'].removeClass('marked');
            if ( Contribute.isDefaultText(Contribute.form['wikiText'].val()) ) {
                Contribute.buttons['confirm'].addClass('marked');
                return false;
            }
            Parser.parse(Contribute.form['wikiText'].val());
            if ( Parser.errorState == true ) {
                return false;
            }
           /* Parser.parse(Contribute.form['wikiTextAlt'].val());
            if ( Parser.errorState == true ) {
                return false;
            }*/
        return true;
        case 'derivateStepOne':
        return true;
        case 'derivateFinished':
        	
            Contribute.buttons['confirm'].removeClass('marked');
            if ( Contribute.isDefaultText(Contribute.form['wikiText'].val()) ) {
                Contribute.buttons['confirm'].addClass('marked');
                return false;
            }
            Parser.parse(Contribute.form['wikiText'].val());
            if ( Parser.errorState == true ) {
                return false;
            }
           /* Parser.parse(Contribute.form['wikiTextAlt'].val());
            if ( Parser.errorState == true ) {
                return false;
            }*/
        return true;
    }
};



ClassContribute.prototype.markButton = function (type) {
    for ( b in Contribute.buttons ) {
        Contribute.buttons[b].removeClass('marked');
        if ( b == type || b == 'confirm' ) {
            Contribute.buttons[b].addClass('marked');
        }
    }
};



ClassContribute.prototype.setArg = function (type) {
    Contribute.formContainer.show();
    for ( f in Contribute.form ) {
        Contribute.form[f].show();
        if ( f == 'wikiText' ) {
            if ( Contribute.isDefaultText(Contribute.form[f].val()) ) {
                Contribute.form[f]
                    .val(Contribute.defaultText['arg'][f])
                    .trigger('keyup');
            }
        }
        if ( f == 'wikiTextAlt' ) {
            if ( Contribute.isDefaultText(Contribute.form[f].val()) ) {
                Contribute.form[f]
                    .val(Contribute.defaultText['arg'][f])
                    .trigger('keyup');
            }
            Contribute.form[f]
                .attr('disabled',true);
        }
        if ( f == 'type' ) {
            Contribute.form[f].attr('value',type);
        }
    }
    return false;
};

ClassContribute.prototype.setCon = function () {
    Contribute.markButton('newCon');
    Contribute.setArg('con');
    return false;
};

ClassContribute.prototype.setNeut = function () {
    Contribute.markButton('newNeut');	
    Contribute.setArg('neut');
    return false;
};

ClassContribute.prototype.setPro = function () {
    Contribute.markButton('newPro');
    Contribute.setArg('pro');
    return false;
};
//ClassContribute.prototype.setViewEditText
ClassContribute.prototype.showEditor = function () {
	Contribute.form={};	
	Contribute.overlay = $('#overlay')
    	.click(Contribute.close)
    	.show();
	Contribute.overlay.empty();
	Contribute.container = $('<div>')
    	.addClass('contributeContainer')
    	.click(function () {return false;})
    	.appendTo(Contribute.overlay);
	Contribute.formContainer = $('<div>')
    	.addClass('formContainer')	
    	.hide()
    	.appendTo(Contribute.container);
    Contribute.form = {};
    Contribute.form['temp'] ="";
    Contribute.form['wikiText'] = $('<textarea>')
        .addClass('formElement')
        .appendTo(Contribute.formContainer)
        .keyup(function () {
            Contribute.checkDone();
            Contribute.form['wikiTextDisplay']
                .empty();
            if ( $(this).val() != '' ) {
                Contribute.form['wikiTextDisplay']
                    .html(Parser.parse($(this).val()));
            }
        })
        .hide();
    Contribute.form['wikiTextDisplay'] = $('<div>')
        .addClass('formElement')
        .appendTo(Contribute.formContainer)
        .hide();
    Contribute.form['type'] = $('<input type="hidden">')
        .appendTo(Contribute.formContainer);
	Contribute.buttons = {};
	
	Contribute.container.attr('style','width:100%; right:0px;margin-right:0px;bottom:50px;top:95px;')
	Contribute.form['wikiText'].attr('style','width:46%; margin:2%;float:right;height:90%;')
	Contribute.form['wikiTextDisplay'].attr('style','width:46%;margin:2%;')
    Contribute.markButton('newText');
	Contribute.form['wikiText'].show();
    Contribute.formContainer.show();


};


ClassContribute.prototype.setViewNewPro = function () {
	Contribute.showEditor();
	Contribute.formType='pro';
	Contribute.buttons['confirm']=$('<div>Abschicken</div>')
		.addClass('button')
		.addClass('marked')
		.attr('style','margin-bottom: 10px;')
		.click(Contribute.submit)
		.appendTo(Contribute.container);
	$('<div>Abbrechen</div>')
		.addClass('button')
		.attr('style','margin-bottom: 10px;')
		.attr('id','cancelbutton')
		.click(Contribute.close)
		.appendTo(Contribute.container);
	Contribute.form['wikiText']
		.val(Contribute.defaultText['pro']['wikiText'])
    	.trigger('keyup');
	return false;
};

ClassContribute.prototype.setViewNewCon = function () {
	Contribute.showEditor();
	Contribute.formType='con';
	Contribute.buttons['confirm']=$('<div>Abschicken</div>')
		.addClass('button')
		.addClass('marked')
		.attr('style','margin-bottom: 10px;')
		.click(Contribute.submit)
		.appendTo(Contribute.container);
	$('<div>Abbrechen</div>')
		.addClass('button')
		.attr('style','margin-bottom: 10px;')
		.attr('id','cancelbutton')
		.click(Contribute.close)
		.appendTo(Contribute.container);
	Contribute.form['wikiText']
		.val(Contribute.defaultText['con']['wikiText'])
    	.trigger('keyup');
	return false;
};
ClassContribute.prototype.setViewNewNeut = function () {
	Contribute.showEditor();
	Contribute.formType='neut';
	Contribute.buttons['confirm']=$('<div>Abschicken</div>')
		.addClass('button')
		.addClass('marked')
		.attr('style','margin-bottom: 10px;')
		.click(Contribute.submit)
		.appendTo(Contribute.container);
	$('<div>Abbrechen</div>')
		.addClass('button')
		.attr('style','margin-bottom: 10px;')
		.attr('id','cancelbutton')
		.click(Contribute.close)
		.appendTo(Contribute.container);
	Contribute.form['wikiText']
		.val(Contribute.defaultText['neut']['wikiText'])
    	.trigger('keyup');
	return false;
};

ClassContribute.prototype.setViewDerivateText = function () {
	Contribute.showEditor();
	Contribute.formType='derivateStepOne';
	Contribute.buttons['confirm']=$('<div>Weiter</div>')
		.addClass('button')
		.addClass('marked')
		.attr('style','margin-bottom: 10px;')
		.click(Contribute.submit)
		.appendTo(Contribute.container);
	$('<div>Abbrechen</div>')
		.addClass('button')
		.attr('style','margin-bottom: 10px;')
		.attr('id','cancelbutton')
		.click(Contribute.close)
		.appendTo(Contribute.container);
	Contribute.form['wikiText']
		.val(Contribute.defaultText['derivate']['wikiTextReason'])
    	.trigger('keyup');
	return false;
};

ClassContribute.prototype.setViewDerivateTextStepTwo = function () {
	Contribute.showEditor();
	Contribute.formType='derivateFinished';
	Contribute.buttons['confirm']=$('<div>Absenden</div>')
		.addClass('button')
		.addClass('marked')
		.attr('style','margin-bottom: 10px;')
		.click(Contribute.submit)
		.appendTo(Contribute.container);
	$('<div>Abbrechen</div>')
		.addClass('button')
		.attr('style','margin-bottom: 10px;')
		.attr('id','cancelbutton')
		.click(Contribute.close)
		.appendTo(Contribute.container);
	Contribute.form['wikiText']
		.val(Contribute.defaultText['derivate']['wikiText'])
    	.trigger('keyup');
    return false;
};

ClassContribute.prototype.setViewNewSection = function () {
	Contribute.showEditor();
	Contribute.formType='text';
	Contribute.buttons['confirm']=$('<div>Abschicken</div>')
		.addClass('button')
		.addClass('marked')
		.attr('style','margin-bottom: 10px;')
		.click(Contribute.submit)
		.appendTo(Contribute.container);
	$('<div>Abbrechen</div>')
		.addClass('button')
		.attr('style','margin-bottom: 10px;')
		.attr('id','cancelbutton')
		.click(Contribute.close)
		.appendTo(Contribute.container);
	Contribute.form['wikiText']
    	.val(Contribute.defaultText['text']['wikiText'])
    	.trigger('keyup');
	
	return false;

    
};
//ClassContribute.prototype.setViewEditText
ClassContribute.prototype.setViewAlternativeText = function () {
	Contribute.showEditor();
	Contribute.formType='alternative';
	Contribute.buttons['confirm']=$('<div>Abschicken</div>')
		.addClass('button')
		.addClass('marked')
		.attr('style','margin-bottom: 10px;')
		.click(Contribute.submit)
		.appendTo(Contribute.container);
	$('<div>Abbrechen</div>')
		.addClass('button')
		.attr('style','margin-bottom: 10px;')
		.attr('id','cancelbutton')
		.click(Contribute.close)
		.appendTo(Contribute.container);
	Contribute.form['wikiText']
    	.val(Contribute.defaultText['alternative']['wikiText'])
    	.trigger('keyup');
	
	return false;

	
    
};

ClassContribute.prototype.submit = function () {
//TODO: Mehrfach senden verhindern
	

        if ( Contribute.checkDone() != true ) {
            alert("not done!");
            return false;
        }
        var data = {};
        switch ( Contribute.formType ) {
            case 'pro':
                data['wikiText'] = Contribute.form['wikiText'].val();
                data['argumentType'] = 'pro';
            break;
            case 'neut':
                data['wikiText'] = Contribute.form['wikiText'].val();
                data['argumentType'] = 'neut';
            break;
            case 'con':
                data['wikiText'] = Contribute.form['wikiText'].val();
                data['argumentType'] = 'con';
            break;
            case 'text':
                data['wikiText'] = Contribute.form['wikiText'].val();
            break;
            case 'alternative':
            	data['wikiText'] = Contribute.form['wikiText'].val();
            break;
            case 'derivateStepOne':
            
            		
                Contribute.temp = Contribute.form['wikiText'].val();
                Contribute.setViewDerivateTextStepTwo();
            	return false;
            break;
            case 'derivateFinished':
            
            	data['wikiText'] = Contribute.temp;
            	data['wikiTextAlternative'] = Contribute.form['wikiText'].val();
            	data['argumentType'] = 'con';
            break;
            
            
        }
        
        

        RqHandler.post({
            url: '.json_storeText' + Controller.getPosition(),
            data: data,
            success: Contribute.callback,
        });
        return false;
}

ClassContribute.prototype.callback = function(data) {
    if ( data['storeTextResponse'] == undefined
        || data['storeTextResponse']['path'] == undefined ) {
        return false;
    }
    Contribute.overlay.hide();
    Controller.loadIndex(data['storeTextResponse']['path'].replace(/\.(pro|con|neut)\.\d+/g,''));
}