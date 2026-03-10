/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.LibroReclamaciones = publicWidget.Widget.extend({
    selector: ".libro-reclamaciones",
    events:Object.assign({},{
        'change input[name="consumer_type"]':'change_consumer_type',
        'change select[name="consumer_state_id"]':'change_consumer_state',
        'change select[name="consumer_province_id"]':'change_consumer_province',
        'change input[name="consumer_younger"]':'change_consumer_younger'
    }),

    change_consumer_type:function(ev){
        var self = this;
        var company_type = $(ev.currentTarget).val()
        if(company_type === 'individual'){
            $(self.$el).find("#consumer_company_name").addClass("d-none")
            $(self.$el).find("#consumer_company_document").addClass("d-none")
        }else if(company_type === 'company'){
            $(self.$el).find("#consumer_company_name").removeClass("d-none")
            $(self.$el).find("#consumer_company_document").removeClass("d-none")
        }
    },
    change_consumer_state: function(ev){
        var self = this
        var consumer_state_id = $(ev.currentTarget).val()
        rpc('/get-provincia-libro-reclamaciones',{'departamento': consumer_state_id})
            .then(async function (data) {
                await $(self.$el).find("select[name='consumer_province_id']").empty()
                await $(self.$el).find("select[name='consumer_district_id']").empty()
                $(self.$el).find("select[name='consumer_province_id']").append($('<option selected="" disabled="">Seleccionar</option>'))
                $(self.$el).find("select[name='consumer_district_id']").append($('<option selected="" disabled="">Seleccionar</option>'))
                for (let i = 0; i < data.length; i++) {
                    $(self.$el).find("select[name='consumer_province_id']").append($('<option /}>').val(data[i].id).text(data[i].name));
                }
        })
    },
    change_consumer_province:function(ev){
        var self = this
        var consumer_province_id = $(ev.currentTarget).val()
        rpc('/get-distrito-libro-reclamaciones',{'provincia': consumer_province_id})
            .then(async function (data) {
                await $(self.$el).find("select[name='consumer_district_id']").empty()
                $(self.$el).find("select[name='consumer_district_id']").append($('<option selected="" disabled="">Seleccionar</option>'))
                for (let i = 0; i < data.length; i++) {
                    $(self.$el).find("select[name='consumer_district_id']").append($('<option /}>').val(data[i].id).text(data[i].name));
                }
        })
    },
    change_consumer_younger:function(ev){
        var self = this;
        var consumer_younger = $(ev.currentTarget).is(':checked')
        console.log(consumer_younger)
        if(consumer_younger){
            $(self.$el).find("#consumer_younger_title").removeClass("d-none")
            $(self.$el).find("#consumer_younger_content").removeClass("d-none")
        }else{
            $(self.$el).find("#consumer_younger_title").addClass("d-none")
            $(self.$el).find("#consumer_younger_content").addClass("d-none")
        }
    }
});