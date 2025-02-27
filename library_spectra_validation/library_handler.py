from matchms.importing import load_spectra
from matchms.filtering.SpectrumProcessor import SpectrumProcessor
from filters import PRIMARY_FILTERS

class LibraryHandler:
    """Stores the 3 different types of spectra. Correct, repaired, wrong.
    Has internal organization using spectrum ids"""

    def __init__(self, f, pipeline):
        #todo modify default pipeline 
        metadata_field_harmonization = SpectrumProcessor(predefined_pipeline=None,
                                                         additional_filters=PRIMARY_FILTERS)
        self.spectra = metadata_field_harmonization.process_spectrums(load_spectra(f))
        self.pipeline = pipeline
        self.spectra_dictionary = {
            'valid': None, #[id1, id2,...]
            'repaired': None, #[id1:[modifications],..]
            'invalid': None #also a dictionary
        }
        self.modifications = {} #todo change to Modifications class

    def clean_and_validate_spectrum(self, spectrum_id):
        spectrum = self.spectra[spectrum_id]
        modifications = self.pipeline.run(spectrum)
        spectrum_id.update_spectra_dictionary(spectrum_id, modifications)
        self.modifications.append(modifications)

    def update_spectra_dictionary(self, spectrum_id, modifications):
        self.spectra_dictionary[modifications["spectra_quality"]["updated"]].append(spectrum_id) #valid, repaired,...
        if ((modifications["spectra_quality"]["updated"] != None) &
            (modifications["spectra_quality"]["updated"] != modifications["spectra_quality"]["previous"])):
            self.spectra_dictionary[modifications["spectra_quality"]["previous"]].remove(spectrum_id)

    def run(self):
        for spectrum_id in range(len(self.spectra)):
            self.clean_and_validate_spectrum(spectrum_id)