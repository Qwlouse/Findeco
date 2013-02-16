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
  } };
 
function ClassContribute() {}
var Contribute = new ClassContribute();

ClassContribute.prototype.close = function () {
    if ( $(this).attr('id') == 'overlay' || $(this).attr('id') == 'cancelbutton' ) {
        if ( Contribute.isDefaultText(Contribute.form['wikiText'].val()) != true 
            || Contribute.isDefaultText(Contribute.form['wikiTextAlt'].val()) != true ) {
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

ClassContribute.prototype.defaultText = {
    'text': {
        'wikiText':'= Ersetze dies hier durch einen Titel für deinen Text =' + "\r\n" 
                    + 'Der Titel wird in der Übersicht angezeigt. Dieser Text hier unten ist erst sichtbar wenn jemand auf den verlinkten Titel geklickt hat!' + "\r\n"  + "\r\n" 
                    + 'Der eingegebene Text wird automatisch umgewandelt, du siehst also sofort ob deine Formatierung stimmt!',
        'wikiTextAlt':''
    },
    'arg': {
        'wikiText':'= Ersetze dies hier durch einen Titel oder eine Kurzbeschreibung für dein Argument =' + "\r\n" 
                    + 'Der Titel beziehungsweise die Kurzbeschreibung ist in der Übersicht der Argumente sichtbar. Dieser Text hier unten ist erst sichtbar wenn jemand auf den verlinkten Titel geklickt hat!' + "\r\n"  + "\r\n" 
                    + 'Der eingegebene Text wird automatisch umgewandelt, du siehst also sofort ob deine Formatierung stimmt!',
        'wikiTextAlt':''
    },
    'alt': {
        'wikiText':'= Ersetze dies hier durch einen Titel oder eine Kurzbeschreibung deines Arguments für einen Alternativtext =' + "\r\n" 
                    + 'Der Titel beziehungsweise die Kurzbeschreibung ist in der Übersicht der Argumente sichtbar. Dieser Text hier unten ist erst sichtbar wenn jemand auf den verlinkten Titel geklickt hat!' + "\r\n"  + "\r\n" 
                    + 'Der eingegebene Text wird automatisch umgewandelt, du siehst also sofort ob deine Formatierung stimmt!',
        'wikiTextAlt':'= Ersetze dies hier durch einen Titel für deinen Alternativtext =' + "\r\n" 
                    + 'Der Titel wird in der Übersicht angezeigt. Dieser Text hier unten ist erst sichtbar wenn jemand auf den verlinkten Titel geklickt hat!' + "\r\n"  + "\r\n" 
                    + 'Der eingegebene Text wird automatisch umgewandelt, du siehst also sofort ob deine Formatierung stimmt!'
    }
};

ClassContribute.prototype.handleClick = function (a,b,c) {
    Contribute.overlay = $('#overlay')
        .click(Contribute.close)
        .show();
    Contribute.overlay.empty();
    
    Contribute.container = $('<div>')
        .addClass('contributeContainer')
        .click(function () {return false;})
        .appendTo(Contribute.overlay);
    
    Contribute.buttons = {};
    
    Contribute.buttons['newText'] = $('<div>Neuer Text</div>')
        .addClass('button')
        .attr('style','margin-bottom: 10px;')
        .click(Contribute.setText)
        .appendTo(Contribute.container);
    
    Contribute.argumentContainer = $('<div>')
        .addClass('argumentContainer')
        .appendTo(Contribute.container);
    
    if ( Main.isTypeLoaded('argument') == true ) {
        Contribute.buttons['newPro'] = $('<div>Pro Argument</div>')
            .addClass('button')
            .addClass('argumentButton')
            .click(Contribute.setPro)
            .appendTo(Contribute.argumentContainer);
        Contribute.buttons['newCon'] = $('<div>Contra Argument</div>')
            .addClass('button')
            .addClass('argumentButton')
            .click(Contribute.setCon)
            .appendTo(Contribute.argumentContainer);
        Contribute.buttons['newNeut'] = $('<div>Neutrales Argument</div>')
            .addClass('button')
            .addClass('argumentButton')
            .attr('style','width: 95%;')
            .click(Contribute.setNeut)
            .appendTo(Contribute.argumentContainer);
    }
    if ( Main.isTypeLoaded('text') == true ) {
        Contribute.buttons['newAlt'] = $('<div>Alternativer Text</div>')
            .addClass('button')
            .attr('style','clear: both; margin-bottom: 10px;')
            .click(Contribute.setAlt)
            .appendTo(Contribute.container);
    }
    
    Contribute.formContainer = $('<div>')
        .addClass('formContainer')
        .hide()
        .appendTo(Contribute.container);
    
    Contribute.createForm();
    
    Contribute.buttons['confirm'] = $('<div>Abschicken</div>')
        .addClass('button')
        .addClass('marked')
        .attr('style','margin-bottom: 10px;')
        .click(Contribute.submit)
        .appendTo(Contribute.container);
    
    Contribute.buttons['cancel'] = $('<div>Abbrechen</div>')
        .addClass('button')
        .attr('style','margin-bottom: 10px;')
        .attr('id','cancelbutton')
        .click(Contribute.close)
        .appendTo(Contribute.container);
    
    return false;
};

ClassContribute.prototype.checkDone = function () {
    switch ( Contribute.form['type'].val() ) {
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
        case 'alt':
            Contribute.buttons['confirm'].removeClass('marked');
            if ( Contribute.isDefaultText(Contribute.form['wikiText'].val()) 
                || Contribute.isDefaultText(Contribute.form['wikiTextAlt'].val()) ) {
                Contribute.buttons['confirm'].addClass('marked');
                return false;
            }
            Parser.parse(Contribute.form['wikiText'].val());
            if ( Parser.errorState == true ) {
                return false;
            }
            Parser.parse(Contribute.form['wikiTextAlt'].val());
            if ( Parser.errorState == true ) {
                return false;
            }
        return true;
    }
};

ClassContribute.prototype.createForm = function () {
    Contribute.form = {};
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
    Contribute.form['wikiTextAlt'] = $('<textarea>')
        .addClass('formElement')
        .attr('disabled','disabled')
        .appendTo(Contribute.formContainer)
        .keyup(function () {
            Contribute.checkDone();
            Contribute.form['wikiTextAltDisplay']
                .empty();
            if ( $(this).val() != '' ) {
                Contribute.form['wikiTextAltDisplay']
                    .html(Parser.parse($(this).val()));
            }
        })
        .hide();
    Contribute.form['wikiTextAltDisplay'] = $('<div>')
        .addClass('formElement')
        .appendTo(Contribute.formContainer)
        .hide();
    Contribute.form['type'] = $('<input type="hidden">')
        .appendTo(Contribute.formContainer);
};

ClassContribute.prototype.markButton = function (type) {
    for ( b in Contribute.buttons ) {
        Contribute.buttons[b].removeClass('marked');
        if ( b == type || b == 'confirm' ) {
            Contribute.buttons[b].addClass('marked');
        }
    }
};

ClassContribute.prototype.setAlt = function () {
    Contribute.formContainer.show();
    Contribute.markButton('newAlt');
    for ( f in Contribute.form ) {
        Contribute.form[f].show();
        if ( f == 'wikiText' ) {
            if ( Contribute.isDefaultText(Contribute.form[f].val()) ) {
                Contribute.form[f]
                    .val(Contribute.defaultText['alt'][f])
                    .trigger('keyup');
            }
        }
        if ( f == 'wikiTextAlt' ) {
            if ( Contribute.isDefaultText(Contribute.form[f].val()) ) {
                Contribute.form[f]
                    .val(Contribute.defaultText['alt'][f])
                    .trigger('keyup');
            } else {
                console.log(Contribute.form[f].val());
            }
            Contribute.form[f]
                .attr('disabled',false);
        }
        if ( f == 'type' ) {
            Contribute.form[f].attr('value','alt');
        }
    }
    return false;
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

ClassContribute.prototype.setText = function () {
    Contribute.markButton('newText');
    Contribute.formContainer.show();
    for ( f in Contribute.form ) {
        Contribute.form[f].show();
        if ( f == 'wikiText' ) {
            if ( Contribute.isDefaultText(Contribute.form[f].val()) ) {
                Contribute.form[f]
                    .val(Contribute.defaultText['text'][f])
                    .trigger('keyup');
            }
        }
        if ( f == 'wikiTextAlt' ) {
            if ( Contribute.isDefaultText(Contribute.form[f].val()) ) {
                Contribute.form[f]
                    .val(Contribute.defaultText['text'][f])
                    .trigger('keyup');
            }
            Contribute.form[f]
                .attr('disabled',true);
        }
        if ( f == 'type' ) {
            Contribute.form[f].attr('value','text');
        }
    }
    return false;
};

ClassContribute.prototype.submit = function () {
        if ( Contribute.checkDone() != true ) {
            alert("not done!");
            return false;
        }
        var data = {};
        switch ( Contribute.form['type'].val() ) {
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
            case 'alt':
                data['wikiText'] = Contribute.form['wikiText'].val();
                data['argumentType'] = 'con';
                data['wikiTextAlternative'] = Contribute.form['wikiTextAlt'].val();
            break;
        }
        
        
        $.ajax({
            type: 'POST',
            url: '.json_storeText' + Controller.getPosition(),
            data: data,
            success: Contribute.callback,
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", Helper.getCSRFToken());
            }
        });
        return false;
}

ClassContribute.prototype.callback = function(data) {
    console.log(data);
}