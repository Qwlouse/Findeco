/** It's all Svens fault!!1!11 **********************************************************
 * Copyright (c) 2012 Justus Wingert <justus_wingert@web.de>                            *
 *                                                                                      *
 * This file is part of BasDeM.                                                         *
 *                                                                                      *
 * BasDeM is free software; you can redistribute it and/or modify it under              *
 * the terms of the GNU General Public License as published by the Free Software        *
 * Foundation; either version 3 of the License, or (at your option) any later           *
 * version.                                                                             *
 *                                                                                      *
 * BasDeM is distributed in the hope that it will be useful, but WITHOUT ANY            *
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A      *
 * PARTICULAR PURPOSE. See the GNU General Public License for more details.             *
 *                                                                                      *
 * You should have received a copy of the GNU General Public License along with         *
 * BasDeM. If not, see <http://www.gnu.org/licenses/>.                                  *
 ****************************************************************************************/
 
/****************************************************************************************
 * This Source Code Form is subject to the terms of the Mozilla Public                  *
 * License, v. 2.0. If a copy of the MPL was not distributed with this                  *
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.                             *
 ****************************************************************************************/

function ClassMicroblogging() {}
var Microblogging = new ClassMicroblogging();

ClassMicroblogging.prototype.load = function (position) {
    // console.log('ClassMicroblogging','load');
    DataRegister.get(this.show,'microblogging',position,true);
   
};

ClassMicroblogging.prototype.show = function (data) {
    //This is not really proper... Maybe we need some refactoring
    Microblogging.Container=$('#'+right.getCssID());
    // console.log('ClassMicroblogging','show');
    right.empty();
    right.printData(data);
    Microblogging.formContainer= $('<div>')
        .appendTo(Microblogging.Container)
        .attr('style','position:absolute;bottom:20px;')
    Microblogging.form={};
    Microblogging.form['input'] = $('<textarea>')
        .appendTo(Microblogging.formContainer)
    Microblogging.form['button'] = $('<button>Absenden</button>')
        .attr('title','Hallo')
        .click(function(){Microblogging.submitForm()})
        .appendTo(Microblogging.formContainer);
        
};

ClassMicroblogging.prototype.submitForm = function () {
    data ={};
    data['microBlogText'] = Microblogging.form['input'].val();
    alert('subm'+data['microblogText']);  
    RqHandler.post({
            url: '.json_storeMicroblogPost' + Controller.getPosition(),
            data: data,
            //success: Microblogging.callback,
    });
};
