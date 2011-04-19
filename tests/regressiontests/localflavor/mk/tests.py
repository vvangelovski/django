from django.test import TestCase
from forms import MKPersonForm

class MKLocalflavorTests(TestCase):
    def setUp(self):
        self.form = MKPersonForm({'first_name':'Someone',
                                  'last_name':'Something',
                                  'umcn': '2402983450006',
                                  'municipality':'MK.OD',
                                  'municipality_req':'MK.VE',
                                  'id_number':'A1234567'})

    def test_get_display_methods(self):
        """Test that the get_*_display() methods are added to the model instances."""

        person = self.form.save()
        self.assertEqual(person.get_municipality_display(), 'Ohrid')
        self.assertEqual(person.get_municipality_req_display(), 'Veles')

    def test_municipality_required(self):
        """Test that required MKMunicipalityFields throw appropriate errors."""

        form = MKPersonForm({'first_name':'Someone',
                             'last_name':'Something',
                             'umcn': '2402983450006',
                             'municipality':'MK.OD',
                             'id_number':'A1234567'})
        
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['municipality_req'], [u'This field is required.'])
    
    def test_umcn_invalid(self):
        """Test that UMCNFields throw appropriate errors for invalid UMCNs"""

        form = MKPersonForm({'first_name':'Someone',
                             'last_name':'Something',
                             'umcn': '2402983450007',
                             'municipality':'MK.OD',
                             'municipality_req':'MK.VE',
                             'id_number':'A1234567'})
        
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['umcn'], [u'The UMCN is not valid.'])

        form = MKPersonForm({'first_name':'Someone',
                             'last_name':'Something',
                             'umcn': '3002983450007',
                             'municipality':'MK.OD',
                             'municipality_req':'MK.VE',
                             'id_number':'A1234567'})

        self.assertEqual(form.errors['umcn'],\
                [u'The first 7 digits of the UMCN must represent a valid past date.']) 

    def test_idnumber_invalid(self):
        """Test that MKIdentityCardNumberFields throw appropriate errors for invalid values"""

        form = MKPersonForm({'first_name':'Someone',
                             'last_name':'Something',
                             'umcn': '2402983450007',
                             'municipality':'MK.OD',
                             'municipality_req':'MK.VE',
                             'id_number':'A123456a'})
        
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['id_number'],\
                         [u'Identity card numbers must contain'\
                              ' either 4 to 7 digits or an uppercase letter and 7 digits.'])
        
    
        

        

    def test_field_blank_option(self):
        """Test that the empty option is there."""

        municipality_select_html="""<select name="municipality" id="id_municipality">
<option value="">---------</option>
<option value="MK.AD">Aerodrom</option>
<option value="MK.AR">Ara\xc4\x8dinovo</option>
<option value="MK.BR">Berovo</option>
<option value="MK.TL">Bitola</option>
<option value="MK.BG">Bogdanci</option>
<option value="MK.VJ">Bogovinje</option>
<option value="MK.BS">Bosilovo</option>
<option value="MK.BN">Brvenica</option>
<option value="MK.BU">Butel</option>
<option value="MK.VA">Valandovo</option>
<option value="MK.VL">Vasilevo</option>
<option value="MK.VV">Vev\xc4\x8dani</option>
<option value="MK.VE">Veles</option>
<option value="MK.NI">Vinica</option>
<option value="MK.VC">Vrane\xc5\xa1tica</option>
<option value="MK.VH">Vrap\xc4\x8di\xc5\xa1te</option>
<option value="MK.GB">Gazi Baba</option>
<option value="MK.GV">Gevgelija</option>
<option value="MK.GT">Gostivar</option>
<option value="MK.GR">Gradsko</option>
<option value="MK.DB">Debar</option>
<option value="MK.DA">Debarca</option>
<option value="MK.DL">Del\xc4\x8devo</option>
<option value="MK.DK">Demir Kapija</option>
<option value="MK.DM">Demir Hisar</option>
<option value="MK.DE">Dolneni</option>
<option value="MK.DR">Drugovo</option>
<option value="MK.GP">Gjor\xc4\x8de Petrov</option>
<option value="MK.ZE">\xc5\xbdelino</option>
<option value="MK.ZA">Zajas</option>
<option value="MK.ZK">Zelenikovo</option>
<option value="MK.ZR">Zrnovci</option>
<option value="MK.IL">Ilinden</option>
<option value="MK.JG">Jegunovce</option>
<option value="MK.AV">Kavadarci</option>
<option value="MK.KB">Karbinci</option>
<option value="MK.KX">Karpo\xc5\xa1</option>
<option value="MK.VD">Kisela Voda</option>
<option value="MK.KH">Ki\xc4\x8devo</option>
<option value="MK.KN">Kon\xc4\x8de</option>
<option value="MK.OC">Ko\xc4\x87ani</option>
<option value="MK.KY">Kratovo</option>
<option value="MK.KZ">Kriva Palanka</option>
<option value="MK.KG">Krivoga\xc5\xa1tani</option>
<option value="MK.KS">Kru\xc5\xa1evo</option>
<option value="MK.UM">Kumanovo</option>
<option value="MK.LI">Lipkovo</option>
<option value="MK.LO">Lozovo</option>
<option value="MK.MR">Mavrovo i Rostu\xc5\xa1a</option>
<option value="MK.MK">Makedonska Kamenica</option>
<option value="MK.MD">Makedonski Brod</option>
<option value="MK.MG">Mogila</option>
<option value="MK.NG">Negotino</option>
<option value="MK.NV">Novaci</option>
<option value="MK.NS">Novo Selo</option>
<option value="MK.OS">Oslomej</option>
<option value="MK.OD" selected="selected">Ohrid</option>
<option value="MK.PE">Petrovec</option>
<option value="MK.PH">Peh\xc4\x8devo</option>
<option value="MK.PN">Plasnica</option>
<option value="MK.PP">Prilep</option>
<option value="MK.PT">Probi\xc5\xa1tip</option>
<option value="MK.RV">Radovi\xc5\xa1</option>
<option value="MK.RN">Rankovce</option>
<option value="MK.RE">Resen</option>
<option value="MK.RO">Rosoman</option>
<option value="MK.AJ">Saraj</option>
<option value="MK.SL">Sveti Nikole</option>
<option value="MK.SS">Sopi\xc5\xa1te</option>
<option value="MK.SD">Star Dojran</option>
<option value="MK.NA">Staro Nagori\xc4\x8dane</option>
<option value="MK.UG">Struga</option>
<option value="MK.RU">Strumica</option>
<option value="MK.SU">Studeni\xc4\x8dani</option>
<option value="MK.TR">Tearce</option>
<option value="MK.ET">Tetovo</option>
<option value="MK.CE">Centar</option>
<option value="MK.CZ">Centar-\xc5\xbdupa</option>
<option value="MK.CI">\xc4\x8cair</option>
<option value="MK.CA">\xc4\x8ca\xc5\xa1ka</option>
<option value="MK.CH">\xc4\x8ce\xc5\xa1inovo-Oble\xc5\xa1evo</option>
<option value="MK.CS">\xc4\x8cu\xc4\x8der-Sandevo</option>
<option value="MK.ST">\xc5\xa0tip</option>
<option value="MK.SO">\xc5\xa0uto Orizari</option>
</select>"""

        
        self.assertEqual(str(self.form['municipality']), municipality_select_html)

