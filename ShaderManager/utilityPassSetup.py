import pymel.core as pc
import mtoa.aovs as aovs

# Creates shaders
shadowProxy = pc.shadingNode('surfaceShader', asShader=1, name="Shadow_SHD")
aoProxy = pc.shadingNode('surfaceShader', asShader=1, name="AO_SHD")

shadowShd = pc.shadingNode('aiShadowCatcher', asShader=1, name="ShadowNode")
aoShd = pc.shadingNode('aiAmbientOcclusion', asShader=1, name="AoNode")

aoShd.outColor >> aoProxy.outColor
shadowShd.outColor >> shadowProxy.outColor

# Creates AOV

aovs.AOVInterface().addAOV("env_shadows")
aovs.AOVInterface().addAOV("env_ao")

envShdAov = pc.PyNode('aiAOV_env_shadows')
envAoAov = pc.PyNode('aiAOV_env_ao')

aoProxy.outColor >> envAoAov.defaultValue
shadowProxy.outColor >> envShdAov.defaultValue

# Set some values
aoShd = pc.PyNode(aoShd)
shadowShd = pc.PyNode(shadowShd)

aoShd.samples.set(8)
shadowShd.shadowColor.set([1,1,1])


