#Author-Autodesk Inc.
#Description-Etract BOM information from active design.

import adsk.core, adsk.fusion, traceback, re



def walkThrough(bom):
    mStr = ''
    for item in bom:
        mStr += '{:15s} {:10s}'.format(str(item['instances']),  item['name']) + '\n'
    return mStr

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        title = 'Extract BOM'
        if not design:
            ui.messageBox('No active design', title)
            return

        # Get all occurrences in the root component of the active design
        root = design.rootComponent
        occs = root.allOccurrences
        
        # Gather information about each unique component
        bom = []
        for occ in occs:
            comp = occ.component
            jj = 0
            for bomI in bom:
                if bomI['component'] == comp:
                    # Increment the instance count of the existing row.
                    bomI['instances'] += 1
                    break
                jj += 1

            if jj == len(bom):
                # Gather any BOM worthy values from the component
                volume = 0
                bodies = comp.bRepBodies
                for bodyK in bodies:
                    if bodyK.isSolid:
                        volume += bodyK.volume
                

                pattern = r'^9[^_]{8}'
                if re.search(pattern, comp.name) is not None:
                    # Add this component to the BOM
                    bom.append({
                        'component': comp,
                        'name': comp.name.replace("_", " "),
                        'instances': 1,
                        'volume': volume
                    })

        # Display the BOM
        title =  '{:15s} {:10s}'.format('Count',  'Name') + '\n'
        msg = title + '\n' + walkThrough(bom)
        
        ui.messageBox(msg, 'McMASTER-CARR Order Export')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

