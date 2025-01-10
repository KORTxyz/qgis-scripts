"""
Download Datafordeler - Stednavne
Name : DownloadDatafordelerStednavne
Group : ETL
With QGIS : 34000
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterFeatureSink

import processing


class DownloadDatafordelerStednavne(QgsProcessingAlgorithm):
    Entity = ['Adgangspunkt','AndenTopografiFlade','AndenTopografiPunkt','Bebyggelse','Begravelsesplads','Bygning','Campingplads','FaergeruteLinje','FaergerutePunkt','Farvand','Fortidsminde','Friluftsbad','Havnebassin','Idraetsanlaeg','Jernbane','Landskabsform','Lufthavn','Naturareal','Navigationsanlaeg','Restriktionsareal','Rute','Sevaerdighed','Soe','Standsningssted','Stednavn','Terraenkontur','UbearbejdetNavnFlade','UbearbejdetNavnLinje','UbearbejdetNavnPunkt','UrentFarvand','Vandloeb','Vej'];
    
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterString('username', 'Username', multiLine=False))
        self.addParameter(QgsProcessingParameterString('password', 'Password', multiLine=False))
        self.addParameter(QgsProcessingParameterEnum('entity', 'Entity', options=self.Entity, allowMultiple=False, usesStaticStrings=True))
        self.addParameter(QgsProcessingParameterEnum('type', 'Type', options=['current','bitemporal','temporal'], allowMultiple=False, usesStaticStrings=True))
        self.addParameter(QgsProcessingParameterFeatureSink('Output', 'Output', createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        # Download
        alg_params = {
            'DATA': '',
            'METHOD': 0,  # GET
            'URL': 'https://api.datafordeler.dk/FileDownloads/GetFile?Register=DS&type=Current&LatestTotalForEntity='+ parameters["entity"] +'&format=gpkg&username=' +  parameters["username"]  + '&password=' + parameters["password"] ,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Download'] = processing.run('native:filedownloader', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Unzip
        alg_params = {
            'DIST': '',
            'Zipfile': outputs['Download']['OUTPUT'],
            'FILE': parameters['Output']
        }
        
        outputs['Unzip'] = processing.run('script:Unzipper', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        results['Output'] = outputs['Unzip']['FILE']
        
        return results

    def name(self):
        return 'DownloadDatafordelerStednavne'

    def displayName(self):
        return 'Download Datafordeler - Stednavne'

    def group(self):
        return 'ETL'

    def groupId(self):
        return 'ETL'

    def createInstance(self):
        return DownloadDatafordelerStednavne()
