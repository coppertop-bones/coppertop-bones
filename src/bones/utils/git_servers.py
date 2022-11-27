# **********************************************************************************************************************
#
#                             Copyright (c) 2012-2022 David Briant. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#    disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#    following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. All advertising materials mentioning features or use of this software must display the following acknowledgement:
#    This product includes software developed by the copyright holders.
#
# 4. Neither the name of the copyright holder nor the names of the  contributors may be used to endorse or promote
#    products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# **********************************************************************************************************************


from urllib.request import urlopen
import urllib
HTTPError = urllib.error.HTTPError

from bones.core.sentinels import Missing

# obviously be really really careful downloading Python code from an untrusted source



# **********************************************************************************************************************
# github
# **********************************************************************************************************************

def gitHubContentUrl(details, folders, filename):
    return '/'.join([
        'https://raw.githubusercontent.com/{projectPath}/{branch}/{subPath}'.format(**details),
        '/'.join(folders),
        filename
    ])

def gitHubTreeUrl(details, folders):
    return '/'.join([
        'https://github.com/{projectPath}/tree/{branch}/{subPath}'.format(**details),
        '/'.join(folders),
    ])

def createGitHubDetails(user, project, branch, subPath):
    return dict(projectPath=f'{user}/{project}', branch=branch, subPath=subPath)

def gitHubPyInitFile(gitHubDetails, paths):
    try:
        url = gitHubContentUrl(gitHubDetails, paths, '__init__.py')
        return urlopen(url).read()
    except HTTPError as ex:
        return Missing

def isGitHubNamespaceModule(gitHubDetails, paths):
    try:
        url = gitHubTreeUrl(gitHubDetails, paths)
        result = urlopen(url)
        return True
    except HTTPError as ex:
        return False

def gitHubFile(gitHubDetails, paths, filename):
    try:
        url = gitHubContentUrl(gitHubDetails, paths, filename)
        return urlopen(url).read()
    except HTTPError as ex:
        return Missing



# **********************************************************************************************************************
# gitlab pvt server
# **********************************************************************************************************************

def pvtGitLabContentUrl(details, folders, filename):
    return '/'.join([
        'https://{host}/{projectPath}/-/raw/{branch}/{subPath}'.format(**details),
        '/'.join(folders),
        filename
    ])

def pvtGitLabTreeUrl(details, folders):
    return '/'.join([
        'https://{host}/{projectPath}/-/tree/{branch}/{subPath}'.format(**details),
        '/'.join(folders),
    ])

def createPvtGitLabDetails(host, projectPath, branch, subPath):
    return dict(host=host, projectPath=projectPath, branch=branch, subPath=subPath)

def pvtGitLabPyInitFile(pvtGitLabDetails, paths):
    try:
        url = pvtGitLabContentUrl(pvtGitLabDetails, paths, '__init__.py')
        content = urlopen(url).read()
        if content.startswith(b'<!DOCTYPE'):
            return Missing
        else:
            return content
    except HTTPError as ex:
        return Missing

def isPvtGitLabNamespaceModule(pvtGitLabDetails, paths):
    try:
        url = pvtGitLabTreeUrl(pvtGitLabDetails, paths)
        content = urlopen(url)
        return True
    except HTTPError as ex:
        return False

def pvtGitLabFile(pvtGitLabDetails, paths, filename):
    try:
        url = pvtGitLabContentUrl(pvtGitLabDetails, paths, filename)
        return urlopen(url).read()
    except HTTPError as ex:
        return Missing

