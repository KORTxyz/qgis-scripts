"""

Name : udtrækområde
Group : 
With QGIS : 34000
"""

from qgis.core import QgsProcessing, QgsProcessingAlgorithm

from qgis.core import QgsProcessingParameterFile, QgsProcessingParameterFile

from qgis.core import QgsProcessingOutputString, QgsProcessingOutputVariant

from qgis.core import QgsProcessingUtils, QgsMessageLog

from qgis.core import QgsZipUtils

from qgis.core  import Qgis

import processing


class Unzipper(QgsProcessingAlgorithm):
    
    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile('Zipfile',
                'File to be unzipped', 
                behavior=QgsProcessingParameterFile.File, 
                fileFilter='Zip file (*.zip)'
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFile('DIST', 'Destination to unzip files to', optional=True, behavior=QgsProcessingParameterFile.Folder, defaultValue=None)
        )
        
        self.addOutput(
            QgsProcessingOutputVariant('DISTFILES', 'List of unzipped files')
        )


    def processAlgorithm(self, parameters, context, model_feedback):
        results = {}
        outputs = {}
        
        if not parameters['DIST']:
            parameters['DIST'] = QgsProcessingUtils.tempFolder()
   
        outputs['UnzippedFiles'] = QgsZipUtils.unzip(parameters['Zipfile'],parameters['DIST'])
        
        results['DISTFILES'] = outputs['UnzippedFiles'][1]

        
        return results

    def name(self):
        return 'Unzipper'

    def displayName(self):
        return 'Unzipper'

    def group(self):
        return 'ETL'

    def groupId(self):
        return 'ETL'

    def shortHelpString(self):
        return "Unzip file"

    def createInstance(self):
        return Unzipper()
