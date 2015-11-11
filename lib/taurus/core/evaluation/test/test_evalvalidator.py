#!/usr/bin/env python

#############################################################################
##
## This file is part of Taurus
##
## http://taurus-scada.org
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
## Taurus is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Taurus is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

"""Test for taurus.core.evaluation.test.test_evalvalidator..."""


__docformat__ = 'restructuredtext'

import taurus
from taurus.external import unittest
from taurus.core.test import (valid, invalid, names,
                              AbstractNameValidatorTestCase)
from taurus.core.evaluation.evalvalidator import (EvaluationAuthorityNameValidator,
                                                  EvaluationDeviceNameValidator,
                                                  EvaluationAttributeNameValidator)

try:
    authority = taurus.Factory('tango').getAuthority()
    default_tango_authority = authority.getSimpleName()
    reason = None
except:
    default_tango_authority = None
    reason = "Tango scheme is not available"
#===============================================================================
# Tests for Eval Authority  name validation
#===============================================================================
@valid(name='eval://localhost')
@invalid(name='eval://foo:10000')
@invalid(name='eval://user@foo:10000')
@invalid(name='eval://user@localhost')
@invalid(name='eval://localhost/')
@invalid(name='eval://localhost/?')
@invalid(name='eval:foo')
@valid(name='eval://db=foo', strict=False)
@invalid(name='eval://db=foo', strict=True)
@valid(name='//db=foo', strict=False)  #using implicit scheme!
 
@names(name='eval://localhost',
       out=('eval://localhost', '//localhost', 'localhost'))
 
@names(name='//localhost', #using implicit scheme!
       out=('eval://localhost', '//localhost', 'localhost'))
class EvaluationAuthValidatorTestCase(AbstractNameValidatorTestCase,
                                 unittest.TestCase):
    validator = EvaluationAuthorityNameValidator
 
 
#===============================================================================
# Tests for Eval Device name validation
#===============================================================================
@invalid(name='eval:foo')
@valid(name='eval:@foo')
@valid(name='eval:@mymod.Myclass', groups={'devname':'@mymod.Myclass'})
@valid(name='eval:@mymod.mysubmod.Myclass')
@valid(name='eval:/@foo', groups={'devname':'@foo', 'path':'/@foo'})
@valid(name='eval://localhost/@foo')
@valid(name='eval:@ foo', groups={'devname':'@ foo'})
@invalid(name='eval:@foo?')
@valid(name='eval://dev=foo', strict=False)
@valid(name='eval://db=localhost;dev=foo', strict=False)
@invalid(name='eval://@foo', strict=False)
@invalid(name='eval://db=localhost;@foo', strict=False)
@invalid(name='eval://localhost;dev=foo', strict=False)
@valid(name='eval:@foo')
@invalid(name='eval://a/b', strict=True)
@invalid(name='eval://d')
 
@names(name='eval://localhost/@foo',
       out=('eval://localhost/@foo', '@foo', 'foo'))

@names(name='eval://dev=foo',
       out=('eval://localhost/@foo', '@foo', 'foo'))

class EvaluationDevValidatorTestCase(AbstractNameValidatorTestCase,
                                 unittest.TestCase):
    validator = EvaluationDeviceNameValidator
 
  
#===============================================================================
# Tests for Eval Attribute name validation
#===============================================================================
 
@valid(name='eval://db=localhost;dev=taurus.core.evaluation.dev_example.FreeSpaceDevice;getFreeSpace("/")/1024/1024',
       strict=False)
@valid(name='eval:1')
#===============================================================================
# this is equivalent to "eval:1". The '/' is part of the path, but not of the 
# attrname
@valid(name='eval:/1', groups={'path':'/1', 'attrname':'1'}) 
#===============================================================================
@valid(name='eval:1/') # "1/" is wrong math, but valid as an attr name!
@valid(name='eval:1/3')
@valid(name='eval:@foo/1')
@valid(name='eval:@mymod.Myclass/1.2', 
       groups={'attrname':'1.2', 'devname':'@mymod.Myclass'})
@valid(name='eval:@foo/1/3')
@valid(name='eval:x=2;y=3;x*y')
@valid(name='eval:@foo/x=2;y=3;x*y')
@valid(name='eval:{tango:a/b/c/d}')
@valid(name='eval:a={tango:a/b/c/d};x=2;a*x', 
       groups={'attrname':'a={tango:a/b/c/d};x=2;a*x',
               '_expr':'a*x',
               '_subst':'a={tango:a/b/c/d};x=2;'})

@valid(name='eval://dev=foo;1', strict=False)
@valid(name='eval://dev=foo;1/3', strict=False)
@valid(name='eval://1/3', strict=False)
@valid(name='eval://dev=foo;x*y?x=2;y=3', strict=False)
@valid(name='eval://x+y+z?x=1;y=2;z=3', strict=False)
@valid(name='eval://a*x?a={tango://a/b/c/d};x=2', strict=False)

@invalid(name='eval://dev=foo;1')
@invalid(name='eval://dev=foo;1/3')
@invalid(name='eval://1/3')
@invalid(name='eval://dev=foo;x*y?x=2;y=3')
@invalid(name='eval://x+y+z?x=1;y=2;z=3')
@invalid(name='eval://a*x?a={tango://a/b/c/d};x=2')

@valid(name='eval://configuration?configuration=1', strict=False) #TODO #1 maybe we can check if the sustitutions can be done
@valid(name='eval://config?config=1', strict=False)
@valid(name='eval://configurationfoo?configurationfoo=1', strict=False)
@valid(name='eval://foo?bar=1', strict=False) #TODO #1
@valid(name='eval:bar=1;foo', strict=False) #TODO #1
@invalid(name='eval://?configurationfoo=1', strict=False)
@invalid(name='eval://?configuration=1', strict=False)
@valid(name='eval://1?configuration=foo1', strict=False)
@valid(name='eval://a?a=1?configuration=label', strict=False)
@valid(name='eval://a+b?a=1;b=2?configuration=label', strict=False)
@valid(name='eval://1?a=1?configuration=label', strict=False)
@valid(name='eval://1?configuration', strict=False)
@valid(name='eval://1?configuration=', strict=False)

@invalid(name='eval://@foo/1')
@valid(name='eval:/@foo/1', groups={'path':'/@foo/1', 'attrname':'1'})
@valid(name='eval:@foo/1', groups={'path':'@foo/1', 'attrname':'1'}) 

# @invalid(name='eval:1#label')
#
# @invalid(name='eval:1?foo')
# @invalid(name='eval:1?configuration')
# @invalid(name='eval:1?configuration=foo')

#===============================================================================

#
# this should be invalid because the reference is a dev name instead of an 
# attr name. But for the moment we do not check such details... 
# #TODO: It could be implemented by using 
#        isValidName(ref, etypes=TaurusElementType.Attribute)
#===============================================================================

@names(name='eval:1', out=('eval://localhost/@DefaultEvaluator/1', '1', '1'))

@names(name='eval:@Foo/1', out=('eval://localhost/@Foo/1', '@Foo/1', '1'))

@names(name='eval:a={tango:a/b/c/d};x=2;a*x', 
       out=('eval://localhost/@DefaultEvaluator/' +\
            'a={tango://%s/a/b/c/d};x=2;a*x' % default_tango_authority,
            'a={tango:a/b/c/d};x=2;a*x',
            'a*x'), test_skip=reason)

@names(name='eval:@Foo/c=1;cos(0)+c', 
       out=('eval://localhost/@Foo/c=1;cos(0)+c',
            '@Foo/c=1;cos(0)+c',
            'cos(0)+c'))

@names(name='eval:@Foo/{NonExistingAlias/foo}+5',
       out=(None,
            '@Foo/{NonExistingAlias/foo}+5',
            'foo+5'))

@names(name='eval:{eval:1}+{eval:2}',
       out=('eval://localhost/@DefaultEvaluator/' +\
            '{eval://localhost/@DefaultEvaluator/1}+' +\
            '{eval://localhost/@DefaultEvaluator/2}',
            '{eval:1}+{eval:2}',
            '1+2'))

@names(name='eval:{eval:{eval:foo=1;foo}}',
       out=('eval://localhost/@DefaultEvaluator/{eval://localhost/' +\
            '@DefaultEvaluator/{eval://localhost/@DefaultEvaluator/foo=1;foo}}',
            '{eval:{eval:foo=1;foo}}',
            'foo'))

@names(name='eval:x=0;x+x-x*x/x+cos(x)-xxx*xy+yx+yxz+x+{w/x/y/x}*x*{eval:x}',
       out=('eval://localhost/@DefaultEvaluator/' +\
            'x=0;x+x-x*x/x+cos(x)-xxx*xy+yx+yxz+x+' +\
            '{tango://%s/w/x/y/x}*x*' % default_tango_authority +\
            '{eval://localhost/@DefaultEvaluator/x}',
            'x=0;x+x-x*x/x+cos(x)-xxx*xy+yx+yxz+x+{w/x/y/x}*x*{eval:x}',
            'x+x-x*x/x+cos(x)-xxx*xy+yx+yxz+x+x*x*x'), test_skip=reason)

#old syntax gets transformed into new one!
@names(name='eval://dev=foo;x*y?x=2;y=3', 
       out=('eval://localhost/@foo/x=2;y=3;x*y',
            '@foo/x=2;y=3;x*y',
            'x*y'))

#old syntax gets transformed into new one!
@names(name='eval://x+x-x*x/x+cos(x)-xxx*xy+yx+yxz+x+{w/x/y/x}*x*{eval:x}?x=0', 
       out=('eval://localhost/@DefaultEvaluator/' +\
            'x=0;x+x-x*x/x+cos(x)-xxx*xy+yx+yxz+x+' +\
            '{tango://%s/w/x/y/x}*x*' % default_tango_authority +\
            '{eval://localhost/@DefaultEvaluator/x}',
            'x=0;x+x-x*x/x+cos(x)-xxx*xy+yx+yxz+x+{w/x/y/x}*x*{eval:x}',
            'x+x-x*x/x+cos(x)-xxx*xy+yx+yxz+x+x*x*x'), test_skip=reason)

@valid(name='eval:1*{eval:x=3;x}')
@valid(name='eval:1*{eval:2*{eval:3}}')
@invalid(name='eval:1*{eval:2*{eval://3}}') # invalid because of non-strict ref
@valid(name='eval:1*{eval:2*{eval://3}}', strict=False)
@invalid(name='eval:{tango:a/b/c}') # invalid:  ref is not an attr!
@invalid(name='eval:{tango:a/b/c}', strict=False) # invalid: ref is not an attr!
@valid(name='eval:{tango:a/b/c/d}') 
@invalid(name='eval:{tango://a/b/c/d}') # invalid because of non-strict ref
@valid(name='eval:{tango://a/b/c/d}', strict=False) # but valid with old syntax

#===============================================================================
# Tests for eval attribute  name validation (when passing cfgkey)
#===============================================================================

@valid(name='eval:1#')
@valid(name='eval:1#units', groups={'cfgkey': 'units'})
@valid(name='eval:{tango:a/b/c/d}*2#')
@valid(name='eval:{tango:a/b/c/d}*2#label')
@valid(name='eval:k=2;a={tango:a/b/c/d};a*k#units')
@valid(name='eval://localhost/@Foo/k=2;a={eval:1};a*k#label')
@valid(name='eval://localhost/@mymod.MyEvalClass/1#label')
@invalid(name='eval:1# ') # invalid because of the trailing space

@names(name='eval:1#units',
       out=('eval://localhost/@DefaultEvaluator/1',
            '1',
            '1', 'units'))

@names(name='eval:@Foo/a={tango:a/b/c/d};x=2;a*x#',
       out=('eval://localhost/@Foo/a={tango://%s/a/b/c/d};x=2;a*x' %\
            default_tango_authority,
            '@Foo/a={tango:a/b/c/d};x=2;a*x',
            'a*x', ''), test_skip=reason)

#old syntax gets transformed into new one!
@names(name='eval://1?configuration=units',
       out=('eval://localhost/@DefaultEvaluator/1',
            '1',
            '1', 'units'))

#old syntax gets transformed into new one!
@names(name='eval://dev=Foo;a*x?a={tango:a/b/c/d};x=2?configuration',
       out=('eval://localhost/@Foo/a={tango://%s/a/b/c/d};x=2;a*x' %\
            default_tango_authority,
            '@Foo/a={tango:a/b/c/d};x=2;a*x',
            'a*x', None), test_skip=reason)

#old syntax gets transformed into new one!
@names(name='eval://dev=Foo;a*x?a={tango:a/b/c/d};x=2?configuration=',
       out=('eval://localhost/@Foo/a={tango://%s/a/b/c/d};x=2;a*x' %\
            default_tango_authority,
            '@Foo/a={tango:a/b/c/d};x=2;a*x',
            'a*x', ''), test_skip=reason)

#old syntax gets transformed into new one!
@names(name='eval://dev=Foo;a*x?a={tango:a/b/c/d};x=2?configuration=label',
       out=('eval://localhost/@Foo/a={tango://%s/a/b/c/d};x=2;a*x' %\
            default_tango_authority,
            '@Foo/a={tango:a/b/c/d};x=2;a*x',
            'a*x', 'label'), test_skip=reason)
class EvaluationAttrValidatorTestCase(AbstractNameValidatorTestCase,
                                      unittest.TestCase):
    validator = EvaluationAttributeNameValidator



if __name__ == '__main__':
    pass
