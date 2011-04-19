# -*- coding: utf-8 -*-
from django.contrib.localflavor.mk.forms import (MKMunicipalitySelect,
            UMCNField,  MKIdentityCardNumberField)
from utils import LocalFlavorTestCase


class MKLocalFlavorTests(LocalFlavorTestCase):
    
    def test_MKMunicipalitySelect(self):
        f = MKMunicipalitySelect()
        out=u'''<select name="municipality">
<option value="MK.AD">Aerodrom</option>
<option value="MK.AR">Ara\u010dinovo</option>
<option value="MK.BR">Berovo</option>
<option value="MK.TL">Bitola</option>
<option value="MK.BG">Bogdanci</option>
<option value="MK.VJ">Bogovinje</option>
<option value="MK.BS">Bosilovo</option>
<option value="MK.BN">Brvenica</option>
<option value="MK.BU">Butel</option>
<option value="MK.VA">Valandovo</option>
<option value="MK.VL">Vasilevo</option>
<option value="MK.VV">Vev\u010dani</option>
<option value="MK.VE">Veles</option>
<option value="MK.NI">Vinica</option>
<option value="MK.VC">Vrane\u0161tica</option>
<option value="MK.VH">Vrap\u010di\u0161te</option>
<option value="MK.GB">Gazi Baba</option>
<option value="MK.GV">Gevgelija</option>
<option value="MK.GT">Gostivar</option>
<option value="MK.GR">Gradsko</option>
<option value="MK.DB">Debar</option>
<option value="MK.DA">Debarca</option>
<option value="MK.DL" selected="selected">Del\u010devo</option>
<option value="MK.DK">Demir Kapija</option>
<option value="MK.DM">Demir Hisar</option>
<option value="MK.DE">Dolneni</option>
<option value="MK.DR">Drugovo</option>
<option value="MK.GP">Gjor\u010de Petrov</option>
<option value="MK.ZE">\u017delino</option>
<option value="MK.ZA">Zajas</option>
<option value="MK.ZK">Zelenikovo</option>
<option value="MK.ZR">Zrnovci</option>
<option value="MK.IL">Ilinden</option>
<option value="MK.JG">Jegunovce</option>
<option value="MK.AV">Kavadarci</option>
<option value="MK.KB">Karbinci</option>
<option value="MK.KX">Karpo\u0161</option>
<option value="MK.VD">Kisela Voda</option>
<option value="MK.KH">Ki\u010devo</option>
<option value="MK.KN">Kon\u010de</option>
<option value="MK.OC">Ko\u0107ani</option>
<option value="MK.KY">Kratovo</option>
<option value="MK.KZ">Kriva Palanka</option>
<option value="MK.KG">Krivoga\u0161tani</option>
<option value="MK.KS">Kru\u0161evo</option>
<option value="MK.UM">Kumanovo</option>
<option value="MK.LI">Lipkovo</option>
<option value="MK.LO">Lozovo</option>
<option value="MK.MR">Mavrovo i Rostu\u0161a</option>
<option value="MK.MK">Makedonska Kamenica</option>
<option value="MK.MD">Makedonski Brod</option>
<option value="MK.MG">Mogila</option>
<option value="MK.NG">Negotino</option>
<option value="MK.NV">Novaci</option>
<option value="MK.NS">Novo Selo</option>
<option value="MK.OS">Oslomej</option>
<option value="MK.OD">Ohrid</option>
<option value="MK.PE">Petrovec</option>
<option value="MK.PH">Peh\u010devo</option>
<option value="MK.PN">Plasnica</option>
<option value="MK.PP">Prilep</option>
<option value="MK.PT">Probi\u0161tip</option>
<option value="MK.RV">Radovi\u0161</option>
<option value="MK.RN">Rankovce</option>
<option value="MK.RE">Resen</option>
<option value="MK.RO">Rosoman</option>
<option value="MK.AJ">Saraj</option>
<option value="MK.SL">Sveti Nikole</option>
<option value="MK.SS">Sopi\u0161te</option>
<option value="MK.SD">Star Dojran</option>
<option value="MK.NA">Staro Nagori\u010dane</option>
<option value="MK.UG">Struga</option>
<option value="MK.RU">Strumica</option>
<option value="MK.SU">Studeni\u010dani</option>
<option value="MK.TR">Tearce</option>
<option value="MK.ET">Tetovo</option>
<option value="MK.CE">Centar</option>
<option value="MK.CZ">Centar-\u017dupa</option>
<option value="MK.CI">\u010cair</option>
<option value="MK.CA">\u010ca\u0161ka</option>
<option value="MK.CH">\u010ce\u0161inovo-Oble\u0161evo</option>
<option value="MK.CS">\u010cu\u010der-Sandevo</option>
<option value="MK.ST">\u0160tip</option>
<option value="MK.SO">\u0160uto Orizari</option>
</select>'''
        
        self.assertEqual( f.render('municipality', 'MK.DL' ), out)
        
    def test_UMCNField(self):
        error_invalid = [u'This field should contain exactly 13 digits.']
        error_checksum = [u'The UMCN is not valid.']
        error_date =  [u'The first 7 digits of the UMCN'\
                           ' must represent a valid past date.']
        valid = {
            '2402983450006': '2402983450006',
            '2803984430038': '2803984430038',
            '1909982045004': '1909982045004',
             }

        invalid = {
            '240298345': error_invalid,
            'abcdefghj': error_invalid,
            '2402082450006': error_date,
            '3002982450006': error_date,
            '2402983450007': error_checksum,
            '2402982450006': error_checksum,
        }
        
        self.assertFieldOutput(UMCNField, valid, invalid)
        
    def test_MKIdentityCardNumberField(self):
        error_invalid  =u'Identity card numbers must contain'\
            ' either 4 to 7 digits or an uppercase letter and 7 digits.'

        valid = {
                'L0018077':'L0018077',
                'A0078315' : 'A0078315',
                }

        invalid = {
                '123': error_invalid,
                'abcdf': error_invalid,
                '234390a': error_invalid,
                }
        
        self.assertFieldOutput(MKIdentityCardNumberField, valid, invalid)









