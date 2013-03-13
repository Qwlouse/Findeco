/** It's all Svens fault!!1!11 **********************************************************
 * Copyright (c) 2012 	Justus Wingert <justus_wingert@web.de>   
 * 						Maik Nauheim 	<findeco@maik-nauheim.de>            
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
/**
 * Constructor
 */
function ClassContribute() {}


	
/**
 * Issues an confirmation request on editor leave and closes the Editor
 */
ClassContribute.prototype.close = function () {
    if ( $(this).attr('id') == 'overlay' || $(this).attr('id') == 'cancelbutton' ) {
        if ( Contribute.isDefaultText(Contribute.form['wikiText'].val()) != true ) {
            if ( confirm(Language.get('cont_leaveForm')) ) {
                $('#overlay').hide();
            }
            return false;
        }
        $('#overlay').hide();
    }
}

/**
 * Checks whether the editor is the default text or not
 * @return bool returns true if the text equals the standard text
 */
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

/**
 * generates dropdown menus for content creation
 * @return JqueryObject representation of dropdown menues
 */
ClassContribute.prototype.generateButtons= function(){
	 // Generate Dropdown menues for new content Creation
	
    DropdownText =$('<div style=" margin: 0 auto; width: 280px;"><div class="btndropdown" style=" width: 135px;"><ul> <li> '+Language.get('cont_textOptions')+'<img src="static/images/dropdown.png" alt="S" title="Sp"> <ul></ul></li></ul></div></div>');
    DropdownArguments =$('<div style=" margin: 0 auto; width: 280px;"><div class="btndropdown" style=" width: 135px;"><ul><li> '+Language.get('cont_arguments')+'<img src="static/images/dropdown.png" alt="S" title="Sp"> <ul></ul></li></ul></div></div><div style="clear:both"></div>');
    
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
    
    
   
    $('<li><div>'+Language.get('cont_proArgument')+'</div></li>')
    	.click(Contribute.setViewNewPro)
    	.appendTo(DropdownArguments.find("ul ul"));
    $('<li><div>'+Language.get('cont_conArgument')+'</div></li>')
    	.click(Contribute.setViewNewCon)
    	.appendTo(DropdownArguments.find("ul ul"));
    $('<li><div>'+Language.get('cont_neutArgument')+'</div></li>')
    	.click(Contribute.setViewNewNeut)
    	.appendTo(DropdownArguments.find("ul ul"));
    
    
    $('<li><div>'+Language.get('cont_newNode')+'</div></li>')
    	.click(Contribute.setViewNewSection )
    	.appendTo(DropdownText.find("ul ul"));
    $('<li><div>'+Language.get('cont_newAlternative')+'</div></li>')
    	.click(Contribute.setViewAlternativeText )
    	.appendTo(DropdownText.find("ul ul"));
    $('<li><div>'+Language.get('cont_newDerivate')+'</div></li>')
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
/**
 * checks whether the current formcontents are Vaild and submitable
 * @return bool returns true if the Form is submitable 
 */
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
        return true;
        case 'derivateStepOne':
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
        
        return true;
    }
};


/**
 * marks buttons depending on formstate
 */
ClassContribute.prototype.markButton = function (type) {
    for ( b in Contribute.buttons ) {
        Contribute.buttons[b].removeClass('marked');
        if ( b == type || b == 'confirm' ) {
            Contribute.buttons[b].addClass('marked');
        }
    }
};




/**
 * shows the wikiText default editor in full width
 */
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
	Contribute.editorTitle = $('<h1>'+Language.get('cont_titleEditor')+'</h2>')
		.appendTo(Contribute.container)
		.addClass('contributeHeadline');
		
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
	Contribute.buttons['confirm']=$('<div>'+Language.get('submit')+'</div>')
		.addClass('button')
		.addClass('marked')
		.attr('style','margin-bottom: 10px;')
		.click(Contribute.submit)
		.appendTo(Contribute.container);
	$('<div>'+Language.get('cancel')+'</div>')
		.addClass('button')
		.attr('style','margin-bottom: 10px;')
		.attr('id','cancelbutton')
		.click(Contribute.close)
		.appendTo(Contribute.container);


};

/**
 * set view and form for pro argument
 */
ClassContribute.prototype.setViewNewPro = function () {
	Contribute.showEditor();
	Contribute.editorTitle.html(Language.get('cont_proArgument'));
	Contribute.formType='pro';
	Contribute.form['wikiText']
		.val(Contribute.defaultText['pro']['wikiText'])
    	.trigger('keyup');
	return false;
};

/**
 * set view and form for con argument
 */
ClassContribute.prototype.setViewNewCon = function () {
	Contribute.showEditor();
	Contribute.editorTitle.html(Language.get('cont_conArgument'));
	Contribute.formType='con';
	Contribute.form['wikiText']
		.val(Contribute.defaultText['con']['wikiText'])
    	.trigger('keyup');
	return false;
};

/**
 * set view and form for neutral argument
 */
ClassContribute.prototype.setViewNewNeut = function () {
	Contribute.showEditor();
	Contribute.editorTitle.html(Language.get('cont_neutArgument'));
	Contribute.formType='neut';
	Contribute.form['wikiText']
		.val(Contribute.defaultText['neut']['wikiText'])
    	.trigger('keyup');
	return false;
};

/**
 * set view and form for text derivation
 */
ClassContribute.prototype.setViewDerivateText = function () {
	Contribute.showEditor();
	Contribute.editorTitle.html(Language.get('cont_derivateDesc'));
	Contribute.formType='derivateStepOne';
	Contribute.buttons['confirm'].html("weiter");
	Contribute.form['wikiText']
		.val(Contribute.defaultText['derivate']['wikiTextReason'])
    	.trigger('keyup');
	return false;
};

/**
 * set view and form for the second step of text derivation
 */
ClassContribute.prototype.setViewDerivateTextStepTwo = function () {
	Contribute.showEditor();
	Contribute.editorTitle.html(Language.get('cont_newDerivate'));
	Contribute.formType='derivateFinished';	
	Contribute.form['wikiText']
		.val(Contribute.defaultText['derivate']['wikiText'])
    	.trigger('keyup');
	DataRegister.get(Contribute.CallbackDerivateTextStepTwo,'text',Controller.position,true);
    return false;
};

/**
 * handler for setting the formtext to the WikiText of the current node and all of his children 
 */
ClassContribute.prototype.CallbackDerivateTextStepTwo = function (data) {
	var temp ="";
	for (p in data['json']['loadTextResponse']['paragraphs']){
			 temp +=" "+ data['json']['loadTextResponse']['paragraphs'][p].wikiText
			
	}
	Contribute.form['wikiText']
		.val(temp)
		.trigger('keyup');
    return false;
};

/**
 * set view and form for new section
 */
ClassContribute.prototype.setViewNewSection = function () {
	Contribute.showEditor();
	Contribute.editorTitle.html(Language.get('cont_newNode'));
	Contribute.formType='text';
	
	Contribute.form['wikiText']
    	.val(Contribute.defaultText['text']['wikiText'])
    	.trigger('keyup');
	return false;

   
};

/**
 * set view and form for alternative Text
 */
ClassContribute.prototype.setViewAlternativeText = function () {
	Contribute.showEditor();
	Contribute.editorTitle.html(Language.get('cont_newAlternative'));
	Contribute.formType='alternative';
	Contribute.form['wikiText']
    	.val(Contribute.defaultText['alternative']['wikiText'])
    	.trigger('keyup');
	
	return false;

	
    
};

/**
 * submit handling logic
 */
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
            	data['wikiTextAlternative'] = Contribute.form['wikiText'].val();
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
        
}
/**
 * callback for submit logic
 */
ClassContribute.prototype.callback = function(data) {
    if ( data['storeTextResponse'] == undefined
        || data['storeTextResponse']['path'] == undefined ) {
        return false;
    }
    Contribute.overlay.hide();
    Controller.loadIndex(data['storeTextResponse']['path'].replace(/\.(pro|con|neut)\.\d+/g,''));
}