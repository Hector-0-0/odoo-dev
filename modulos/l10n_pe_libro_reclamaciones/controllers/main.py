from odoo import http
from odoo.http import request, Response


class LibroReclamacionesController(http.Controller):

    def _fields_required_consumer_type_company(self):
        return ['consumer_company_name', 'consumer_company_document']

    def _fields_required_main(self):
        return ['consumer_type', 'consumer_name', 'consumer_lastname', 'consumer_email', 'consumer_document_type', 'consumer_document',
                'consumer_phone', 'consumer_address', 'consumer_state_id', 'consumer_province_id', 'consumer_district_id',
                'product_type', 'product_code', 'order_name', 'date_order', 'product_name',
                'claim_type', 'claim_amount', 'claim_detail', 'claim_request']

    def _fields_required_consumer_younger(self):
        return ['consumer_younger_name', 'consumer_younger_lastname', 'consumer_younger_document']

    def validate_data_claim(self, claim):
        errors = {}
        for fld in self._fields_required_main():
            if fld not in claim or not bool(claim.get(fld, '')):
                errors[fld] = "Campo obligatorio"

        if claim.get("consumer_type", '') == 'company':
            for fld in self._fields_required_consumer_type_company():
                if fld not in claim or not bool(claim.get(fld, '')):
                    errors[fld] = "Campo obligatorio"

        if claim.get("consumer_younger", False):
            for fld in self._fields_required_consumer_younger():
                if fld not in claim or not bool(claim.get(fld, '')):
                    errors[fld] = "Campo obligatorio"

        state_id = int(claim.get("consumer_state_id", 0))
        province_id = int(claim.get("consumer_province_id", 0))
        district_id = int(claim.get("consumer_district_id", 0))
        res_country_state = request.env["res.country.state"].sudo()
        consumer_state_name = ""
        consumer_province_name = ""
        consumer_district_name = ""
        if state_id:
            consumer_state_id = res_country_state.browse(state_id)
            consumer_state_name = consumer_state_id.name
        if province_id:
            consumer_province_id = res_country_state.browse(province_id)
            consumer_province_name = consumer_province_id.name
        if district_id:
            consumer_district_id = res_country_state.browse(district_id)
            consumer_district_name = consumer_district_id.name

        claim.update({"consumer_state_name": consumer_state_name,
                      "consumer_province_name": consumer_province_name,
                      "consumer_district_name": consumer_district_name})

        return errors, claim


    def process_data_claim(self, claim):
        claim["consumer_younger"] = bool(claim.get("consumer_younger", False))
        if "csrf_token" in claim:
            del claim["csrf_token"]
        if "consumer_state_name" in claim:
            del claim["consumer_state_name"]
        if "consumer_province_name" in claim:
            del claim["consumer_province_name"]
        if "consumer_district_name" in claim:
            del claim["consumer_district_name"]
        if not claim.get("consumer_younger", False):
            for fld in self._fields_required_consumer_younger():
                if fld in claim:
                    del claim[fld]
        if claim.get("consumer_type", False) != 'company':
            for fld in self._fields_required_consumer_type_company():
                if fld in claim:
                    del claim[fld]

        return request.env["libro.reclamaciones"].sudo().create(claim)


    @http.route("/libro-reclamaciones", auth='public', methods=['GET', 'POST'], website=True)
    def LibroReclamacionesForm(self,**args):
        company = request.env.company
        errors = {}
        claim = {}
        country_peru = request.env.ref("base.pe")
        states = request.env["res.country.state"].sudo().search([('country_id','=',country_peru.id)])

        if not bool(args):
            return request.render("l10n_pe_libro_reclamaciones.libro_reclamaciones",{"company":company,
                                                                                        'claim':claim,
                                                                                        'errors':errors,
                                                                                        'states':states})
        else:
            errors, claim = self.validate_data_claim(args)
            if errors:
                return request.render("l10n_pe_libro_reclamaciones.libro_reclamaciones",{"company":company,
                                                                                        'claim':claim,
                                                                                        'errors':errors,
                                                                                        'states':states})
            else:
                #Procesar datos
                claim_obj = self.process_data_claim(claim)
                #Redirigir a pagina de finalización
                return request.redirect(f"/reclamacion-enviada/{claim_obj.name}")


    @http.route('/reclamacion-enviada/<string:code>', type='http', auth='public', website=True)
    def LibroReclamacionesEnviada(self, code):
        return request.render('l10n_pe_libro_reclamaciones.reclamacion_enviada', {"code": code})
           


    @http.route("/get-provincia-libro-reclamaciones",type="json", auth="public", website=True)
    def GetProLibroReclamaciones(self, departamento, **kw):
        cities = request.env["res.city"].sudo().search([('state_id', '=', int(departamento))])
        return cities.mapped(lambda r: {'id': r.id, 'name': r.name})


    @http.route(['/get-distrito-libro-reclamaciones'], type='json', auth="public", website=True)
    def GetDisLibroReclamaciones(self, provincia, **kw):
        districts = request.env['l10n_pe.res.city.district'].sudo().search([('city_id', '=', int(provincia))])
        return districts.mapped(lambda r: {'id': r.id, 'name': r.name})
        #[{'id':'','name':''},{'id':'','name':''},{'id':'','name':''}]