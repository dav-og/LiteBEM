import capytaine as cpt

meshFilename = f'./hemisphere360.nemoh'
body = cpt.FloatingBody.from_file(meshFilename, file_format='nemoh')
        # run nemoh (via capytaine)
body.add_all_rigid_body_dofs() # Add the 6 rigid body's 6 DoFs