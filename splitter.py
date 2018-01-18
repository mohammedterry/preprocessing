def tokenize(raw_text):
    '''
    rule-based algorithm to find sentence boundaries
    without using capital letters
    and can detect two words joint together like.this
    INPUT: large chunk of text
    OUTPUT: text formatted/tokenized so that each word is separated by a space and each sentence is on a newline
    
    Rule 1:  no punctuation inside brackets create a new sentence (...him. Then...) 
    Rule 2a:  .!? followed by '" creates a new sentence starting AFTER the '"
    Rule 2b:  !? followed by anything creates a new sentence BUT not so for .
    Rule 2c:  .!? followed by ., doesnt create a new sentence
    Rule 3a:  1-9 before . doesnt create a new sentence
    Rule 3b:  abbrev. words before . dont usually create new sentences
    Rule 3c: words with normal word endings before . usually create new sentences
    Rule 3d:  closed brackets before . usually create new sentences
    '''
    abbreviations = ['a', 'abbrev.', 'abbrev.', 'abd.', 'aberd.', 'aberdeensh.', 'abl.', 'abol.', 'aborig.', 'abp.', 'abr.', 'abridg.', 'abridgem.', 'absol.', 'absol.', 'abst.', 'abstr.', 'abstr.', 'acad.', 'acc.', 'acc.', 'acc.', 'accept.', 'accomm.', 'accompl.', 'accs.', 'acct.', 'accts.', 'accus.', 'achievem.', 'a.d.', 'ad.', 'add.', 'addit.', 'addr.', 'adj.', 'adj. phr.', 'adjs.', 'adm.', 'adm.', 'admin.', 'admir.', 'admon.', 'admonit.', 'adv.', 'adv.', 'adv.', 'adv.', 'adv.', 'adv.', 'advancem.', 'advb.', 'advert.', 'advoc.', 'advs.', 'advt.', 'advts.', 'aerodynam.', 'aeronaut.', 'aff.', 'affect.', 'affect.', 'afr.', 'agric.', 'agst.', 'alch.', 'alg.', 'alleg.', 'allit.', 'alm.', 'alph.', 'alt.', 'amer.', 'anal.', 'analyt.', 'anat.', 'anc.', 'anecd.', 'ang.', 'angl.', 'anglo-ind.', 'anim.', 'ann.', 'ann.', 'anniv.', 'annot.', 'anon.', 'answ.', 'ant.', 'anthrop.', 'anthropol.', 'antiq.', 'aphet.', 'apoc.', 'apol.', 'app.', 'app.', 'appl.', 'applic.', 'appos.', 'apr.', 'arab.', 'arb.', 'arch.', 'arch.', 'arch.', 'archaeol.', 'archipel.', 'archit.', 'argt.', 'arith.', 'arithm.', 'arrangem.', 'art.', 'artic.', 'artific.', 'artill.', 'ashm.', 'assemb.', 'assoc.', 'assoc. football', 'assyriol.', 'astr.', 'astrol.', 'astron.', 'astronaut.', 'att.', 'attrib.', 'attrib.', 'aug.', 'austral.', 'auth.', 'autobiog.', 'autobiogr.', 'a.v.', 'ayrsh.', 'bacteriol.', 'b.c.', 'b.c.', 'bedford.', 'bedfordsh.', 'bef.', 'bel & dr.', 'belg.', 'berks.', 'berksh.', 'berw.', 'berwicksh.', 'betw.', 'bibliogr.', 'biochem.', 'biog.', 'biogr.', 'biol.', 'bk.', 'bks.', 'bnc', 'bord.', 'bot.', 'bp.', 'braz.', 'brit.', 'bucks.', 'build.', 'bull.', 'bur.', 'c.', 'c.', 'c', 'cal.', 'calc.', 'calend.', 'calif.', 'calligr.', 'camb.', 'cambr.', 'campanol.', 'canad.', 'canterb.', 'capt.', 'cartogr.', 'catal.', 'catech.', 'cath.', 'cent.', 'cent.', 'cent.', 'ceram.', 'cert.', 'certif.', 'cf.', 'ch.', 'chamb.', 'char.', 'charac.', 'chas.', 'chem. engin.', 'chem.', 'chesh.', 'ch. hist.', 'chr.', 'chr.', 'chron.', 'chron.', 'chronol.', 'chrons.', 'cinematogr.', 'circ.', 'civ. law', 'civil engin.', 'cl.', 'cl.', 'class. antiq.', 'class.', 'classif.', 'climatol.', 'clin.', 'cogn. w.', 'col.', 'col.', 'coll.', 'coll.', 'collect.', 'collect.', 'colloq.', 'colloq.', 'coloss.', 'com.', 'com.', 'comb.', 'comb. form', 'combs.', 'comm.', 'comm.', 'comm.', 'comm.', 'comm.', 'commandm.', 'commend.', 'commerc.', 'commiss.', 'comm. law', 'commonw.', 'communic.', 'comp.', 'comp.', 'comp.', 'comp.', 'compan.', 'comp. anat.', 'compar.', 'compar.', 'compend.', 'compl.', 'compl.', 'compos.', 'conc.', 'conc.', 'conch.', 'concl.', 'concr.', 'conf.', 'conf.', 'confid.', 'confl.', 'confut.', 'congr.', 'congreg.', 'congress.', 'conj.', 'conj.', 'conn.', 'cons.', 'consc.', 'consecr.', 'consid.', 'consol.', 'const.', 'constit. hist.', 'constit.', 'constr.', 'contemp.', 'contempl.', 'contempt.', 'contend.', 'content.', 'contin.', 'contr.', 'contr.', 'contradict.', 'contrib.', 'controv.', 'controv.', 'conv.', 'convent.', 'conversat.', 'convoc.', 'cor.', 'cornw.', 'coron.', 'corr.', 'corresp.', 'corresp.', 'counc.', 'courtsh.', 'cpd.', 'craniol.', 'craniom.', 'crim.', 'crim. law', 'crit.', 'crit.', 'crt.', 'crts.', 'cryptogr.', 'crystallogr.', 'ct.', 'ct.', 'cumb.', 'cumberld.', 'cumbld.', 'cycl.', 'cytol.', 'dan.', 'dat.', 'dau.', 'd.c.', 'deb.', 'dec.', 'declar.', 'ded.', 'ded.', 'def.', 'def.', 'def.', 'deliv.', 'dem.', 'demonstr.', 'dep.', 'dep.', 'depred.', 'depredat.', 'dept.', 'derbysh.', 'deriv.', 'derog.', 'descr.', 'deut.', 'devel.', 'devonsh.', 'dial.', 'dial.', 'dict.', 'diffic.', 'dim.', 'direct.', 'dis.', 'disc.', 'discipl.', 'discov.', 'discrim.', 'discuss.', 'diss.', 'dist.', 'distemp.', 'distill.', 'distrib.', 'div.', 'div.', 'divers.', 'dk.', 'doc.', 'doctr.', 'domest.', 'durh.', 'dyslog.', 'e.',
'e.', 'e. afr.', 'e. angl.', 'e. anglian', 'east ind.', 'east.', 'eccl.', 'eccl.', 'eccles.', 'eccles.', 'eccl. hist.', 'eccl. law', 'ecclus.', 'ecol.', 'econ.', 'ed.', 'ed.', 'ed.', 'e.d.d.', 'edin.', 'edinb.', 'educ.', 'edw.', 'e.e.t.s.', 'egypt.', 'egyptol.', 'e. ind.', 'electr.', 'electr. engin.', 'electro-magn.', 'electro-physiol.', 'elem.', 'eliz.', 'elizab.', 'ellipt.', 'emb.', 'embryol.',
'e. midl.', 'emph.', 'encycl.', 'encycl. brit.', 'encycl. metrop.', 'eng.', 'engin.', 'englishw.', 'enq.', 'ent.', 'enthus.', 'entom.', 'entomol.', 'enzymol.', 'eoe', 'ep.', 'eph.', 'ephes.', 'epil.', 'episc.', 'epist.', 'epit.', 'equip.', 'erron.', 'esd.', 'esp.', 'ess.', 'essent.', 'establ.', 'esth.', 'ethnol.', 'etym.', 'etymol.', 'etymol.', 'euphem.', 'eval.', 'evang.', 'even.', 'evid.', 'evol.', 'ex. doc.', 'exalt.', 'exam.', 'exc.', 'exch.', 'exch.', 'exec.', 'exec.', 'exerc.', 'exhib.', 'exod.', 'exped.', 'exper.', 'explan.', 'explic.', 'explor.', 'expos.', 'ezek.', 'f.', 'f.', 'fab.',
'fam.', 'fam.', 'famil.', 'farew.', 'feb.', 'fem.', 'ff.', 'fifesh.', 'fig.', 'fl.', 'footpr.', 'forfarsh.', 'fortif.', 'fortn.', 'found.', 'fr.', 'fr.', 'fr.', 'fragm.', 'fratern.', 'freq.', 'friendsh.', 'fund.', 'furnit.', 'fut.', 'gal.', 'gard.', 'gastron.', 'gaz.', 'gd.', 'gen.', 'gen.', 'gen.', 'gen.', 'geo.', 'geog.', 'geogr.', 'geol.', 'geom.', 'geomorphol.', 'ger.', 'gerund.', 'glac.', 'glasg.', 'glos.', 'gloss.', 'glouc.', 'gloucestersh.', 'gosp.', 'gov.', 'govt.', 'gr.', 'gram.', 'gramm. analysis', 'gt.', 'gynaecol.', 'hab.', 'haematol.', 'hag.', 'hampsh.', 'handbk.', 'hants.', 'heb.', 'heb.', 'hebr.', 'hen.', 'her.', 'herb.', 'heref.', 'hereford.', 'herefordsh.', 'hertfordsh.', 'hierogl.', 'hist.', 'hist.', 'histol.', 'hom.', 'horol.', 'hort.', 'hos.', 'hosp.', 'househ.', 'housek.', 'husb.', 'hydraul.', 'hydrol.', 'ichth.', 'icthyol.', 'ideol.', 'idol.', 'illustr.', 'imag.', 'imit.', 'immunol.', 'imp.', 'imperf.', 'impers.', 'impf.', 'impr.', 'impr.', 'impr.', 'improp.', 'inaug.', 'inclos.', 'ind.', 'ind.', 'ind.', 'ind.', 'indef.', 'indic.', 'indir.', 'industr.', 'industr. rel.', 'infin.', 'infl.', 'infl.', 'innoc.', 'inorg.', 'inq.', 'inst.', 'instr.', 'instr.', 'int.', 'intell.', 'intellect.', 'interc.', 'interj.', 'interl.', 'internat.', 'interpr.', 'interrog.', 'intr.', 'intrans.', 'intro.', 'introd.', 'inv.', 'invent.', 'invent.', 'invertebr.', 'invert. zool.', 'investig.', 'investm.', 'invoc.', 'ir.', 'irel.', 'iron.', 'irreg.', 'isa.', 'ital.', 'jahrb.', 'jam.', 'jam.', 'jan.', 'jap.', 'jas.', 'jas.', 'jer.', 'joc.', 'josh.', 'jrnl.', 'jrnls.', 'jud.', 'judg.', 'jul.', 'jun.', 'jun.', 'jurisd.', 'jurisdict.', 'jurispr.', 'justif.', 'justific.', 'k.', 'kent.', 'kgs.', 'king’s bench div.', 'kingd.', 'knowl.', 'kpr.', 'l.', 'lab.', 'lam.', 'lament', 'lament.', 'lanc.', 'lancash.', 'lancs.', 'lang.', 'langs.', 'lat.', 'ld.', 'lds.', 'lect.', 'leechd.', 'leg.', 'leicest.', 'leicester.', 'leicestersh.', 'leics.', 'let.', 'lett.', 'lev.', 'lex.', 'libr.', 'limnol.', 'lincolnsh.', 'lincs.', 'ling.', 'linn.', 'lit.', 'lit.', 'lithogr.', 'lithol.', 'liturg.', 'll.', 'loe', 'lond.', 'lxx', 'm.', 'macc.', 'mach.', 'mag.', 'magn.', 'mal.', 'man.', 'managem.', 'manch.', 'manip.', 'manuf.', 'mar.', 'masc.', 'mass.', 'math.', 'matt.', 'meas.', 'measurem.', 'mech.', 'med.', 'med.', 'medit.', 'mem.', 'merc.', 'merch.', 'metall.', 'metallif.', 'metallogr.',
'metallogr.', 'metamorph.', 'metaph.', 'metaphor.', 'meteorol.', 'meth.', 'metr. gr.', 'metrop.', 'mex.', 'mic.', 'mich.', 'microbiol.', 'microsc.', 'midl.', 'mil.', 'milit.', 'min.', 'mineral.', 'misc.', 'miscell.', 'mispr.', 'mod.', 'mod.', 'monum.', 'morphol.', 'ms.', 'mss.', 'mt.', 'mtg.', 'mts.', 'munic.', 'munif.', 'munim.', 'mus.', 'mus.', 'myst.', 'myth.', 'mythol.', 'n.', 'n.', 'n.', 'n.', 'n. afr.', 'nah.', 'n. amer.', 'narr.', 'narrat.', 'nat.', 'nat. hist.', 'nat. philos.', 'nat. sci.', 'naut.', 'nav.', 'nav.', 'navig.', 'n. carolina', 'n. dakota', 'n.e.', 'n.e.', 'n.e.d.', 'neh.', 'neighb.', 'nerv.', 'neurol.', 'neurosurg.', 'new hampsh.', 'newc.', 'newspr.', 'n. ir.', 'n. irel.', 'no.', 'nom.', 'non-conf.', 'nonce-wd.', 'nonconf.', 'norf.', 'north.', 'northamptonsh.', 'northants.', 'northumb.', 'northumbld.', 'northumbr.', 'norw.', 'norweg.', 'notts.', 'nov.', 'ns.', 'n.s. wales', 'n.s.w.', 'n.t.', 'nucl.', 'num.', 'numism.', 'n.w.', 'n.w.', 'n.y.', 'n.z.', 'obad.', 'obed.', 'obj.', 'obj.', 'obl.', 'obs.', 'obs.', 'observ.', 'obstet.', 'obstetr.', 'obstetr. med.', 'occas.', 'occas.', 'occup.', 'occurr.', 'oceanogr.', 'oct.', 'oe', 'o.e.d.', 'off.', 'offic.', 'okla.',
'ont.', 'ophthalm.', 'ophthalmol.', 'opp.', 'oppress.', 'opt.', 'orac.', 'ord.', 'ord.', 'org.', 'organ. chem.', 'org. chem.', 'orig.', 'orig.', 'orkn.', 'ornith.', 'ornithol.', 'orthogr.', 'o.t.', 'outl.', 'oxf.', 'oxfordsh.', 'oxon.', 'p.', 'pa.', 'pa.', 'palaeobot.', 'palaeogr.', 'palaeont.', 'palaeontol.', 'pa. pple.', 'paraphr.', 'parasitol.', 'parl.', 'parnass.', 'pass.', 'pa. t.', 'path.',
'pathol.', 'peculat.', 'penins.', 'perf.', 'perf.', 'perh.', 'periodontol.', 'pers.', 'pers.', 'pers.', 'persec.', 'personif.', 'perthsh.', 'pet.', 'petrogr.', 'petrol.', 'pf.', 'pharm.', 'pharmaceut.', 'pharmacol.', 'phil.', 'phil.', 'philad.', 'philem.', 'philipp.', 'philol.', 'philos.', 'phoen.', 'phonet.', 'phonol.', 'photog.', 'photogr.', 'phr.', 'phrenol.', 'phys.', 'physical chem.', 'physical geogr.', 'physiogr.', 'physiol.', 'pict.', 'pict.', 'pl.', 'plur.', 'poet.', 'poet.', 'pol.', 'pol. econ.', 'polit.', 'polytechn.', 'pop.', 'pop.', 'porc.', 'port.', 'poss.', 'poss.', 'posth.', 'postm.', 'pott.', 'ppl.', 'ppl. a.', 'ppl. adj.', 'ppl. adjs.', 'pple.', 'pples.', 'p. r.', 'pr.', 'pract.', 'pract.', 'prec.', 'pred.', 'predic.', 'predict.', 'pref.', 'pref.', 'preh.', 'prehist.', 'prep.', 'prerog.', 'pres.', 'pres.', 'presb.', 'presb.', 'preserv.', 'pres. pple.', 'prim.', 'princ.', 'print.', 'priv.', 'prob.', 'probab.', 'probl.', 'proc.', 'prod.', 'prol.', 'pron.', 'pron.', 'pronunc.', 'pronunc.', 'prop.', 'prop.', 'propr.', 'pros.', 'prov.', 'prov.', 'prov.', 'provid.', 'provinc.', 'provis.', 'pr. pple.', 'ps.', 'pseudo-arch.', 'pseudo-dial.', 'pseudo-sc.', 'psych.', 'psychoanal.', 'psychoanalyt.', 'psychol.', 'psychopathol.', 'pt.', 'publ.', 'publ.', 'purg.', 'q.', 'q.', 'q. eliz.', 'qld.', 'quantum mech.', 'queen’s bench div.', 'quot.', 'quots.', 'q.v.', 'r.', 'radiol.', 'r.a.f.', 'r.c.', 'r.c. church', 'reas.', 'reb.', 'rebell.', 'rec.', 'reclam.', 'recoll.', 'redempt.', 'redupl.', 'ref.', 'ref.', 'refash.', 'refl.', 'refl.', 'refus.', 'refut.', 'reg.', 'reg.', 'regic.', 'regist.', 'regr.', 'rel.', 'rel.', 'rel.', 'relig.', 'reminisc.', 'remonstr.', 'renfrewsh.', 'rep.', 'repr.', 'reprod.', 'rept.', 'repub.', 'res.', 'resid.', 'ret.', 'retrosp.', 'rev.', 'rev.', 'rev.', 'revol.', 'rhet.', 'rhet.', 'rhode isl.', 'rich.', 'r.n.', 'rom.', 'rom.', 'rom. antiq.', 'ross-sh.', 'roxb.', 'roy.', 'rudim.', 'russ.', 's.', 's.', 's. afr.', 'sam.', 'sask.', 'sat.', 'sax.', 'sc.', 'sc.', 'scand.', 's. carolina', 'sch.', 'sci.', 'scot.', 'scotl.', 'script.', 'sculpt.', 's. dakota', 's.e.', 's.e.', 'seismol.', 'sel.', 'sel. comm.', 'select.', 'sept.', 'ser.', 'serm.', 'sess.', 'settlem.', 'sev.', 'shakes.', 'shaks.', 'sheph.', 'shetl.', 'shropsh.', 'sing.', 'soc.', 'sociol.', 'som.', 'song of sol.', 'song sol.', 'sonn.', 'south.', 'sp.', 'span.', 'spec.', 'spec.', 'spec.', 'specif.', 'specim.', 'spectrosc.', 'ss.', 'st.', 'st.', 'staff.', 'stafford.', 'staffordsh.', 'staffs.', 'stand.', 'stat.', 'statist.', 'stock exch.', 'str.', 'stratigr.', 'struct.', 's.t.s.', 'stud.', 'subj.', 'subj.', 'subj.', 'subjunct.', 'subord.', 'subord. cl.', 'subscr.', 'subscript.', 'subseq.', 'subst.', 'suff.', 'suff.', 'superl.', 'suppl.', 'supplic.', 'suppress.', 'surg.', 'surv.', 'sus.', 's.v.', 's.w.', 's.w.', 'syll.', 'symmetr.', 'symp.', 'syst.', 't.', 'taxon.', 'techn.', 'techn.', 'technol.', 'tel.', 'telecomm.', 'telegr.', 'telegr.', 'teleph.', 'teratol.', 'terminol.', 'terrestr.', 'test.', 'textbk.', 'theat.', 'theatr.', 'theol.', 'theoret.', 'thermonucl.', 'thes.', 'thess.', 'tim.', 'tit.', 'topogr.', 'tr.', 'trad.', 'trag.', 'trans.', 'trans.', 'transf.', 'transl.', 'transl.', 'transubstant.', 'trav.', 'treas.', 'treat.', 'treatm.', 'trib.', 'trig.', 'trigonom.', 'trop.', 'troub.', 'troubl.', 'typog.', 'typogr.', 'u.k.', 'ult.', 'univ.', 'unkn.', 'unnat.', 'unoffic.', 'unstr.', 'urin.', 'u.s.', 'u.s.a.f.', 'u.s.s.r.', 'usu.', 'utilit.', 'v.', 'va.', 'vac.', 'valedict.', 'var.', 'varr.', 'vars.', 'vb.', 'vbl.', 'vbl.n.', 'vbl. ns.', 'vbs.', 'veg.', 'veg. phys.', 'veg. physiol.', 'venet.', 'vertebr.', 'vet.', 'vet. med.', 'vet. path.', 'vet. sci.', 'vet. surg.', 'vic.', 'vict.', 'vind.', 'vindic.', 'virg.', 'virol.', 'viz.', 'voc.', 'vocab.', 'vol.', 'vols.', 'voy.', 'v.r.', 'v.rr.', 'vulg.', 'vulg.', 'vulg.', 'w.', 'w.', 'w. afr.', 'warwicksh.', 'wd.', 'wd.', 'west.', 'westm.', 'westmld.', 'westmorld.', 'westmrld.', 'will.', 'wilts.', 'wiltsh.', 'w. ind.', 'w. indies', 'wis.', 'wisd.', 'wisd.', 'wk.', 'wk.', 'wk.', 'wkly.', 'wks.', 'wonderf.', 'worc.', 'worcestersh.', 'worcs.', 'writ.', 'w. va.', 'yearbk.', 'yng.', 'yorks.', 'yorksh.', 'yr.', 'yrs.', 'zech.', 'zeitschr.', 'zeph.', 'zoogeogr.', 'zool.']
    padding = '***'
    brackets = '{[()]}'
    stopmarks = '.!?'
    #punctuation = ',;.!?*:/'
    speechmarks = ''''")]}>'''
    numbers = '0123456789 ' #purposely includes whitespace
    open_brackets = [0,0,0] #{[(<-- without --> }])    
    skip = False
    output = ''

    characters = padding + raw_text.replace('<br />', ' ').replace('\n',' ') + padding #remove newlines etc
    characters = ' '.join(characters.split()) #remove trailing whitespace

    for i in range(3, len(characters)-3):
        character= characters[i]
        output += character
        
        if not(character.isalpha() or character in numbers): #optional formatting to separate fused.words!like-this
                nex = characters[i+1]
                if nex != ' ':
                    output += ' '
        
        if character in brackets:
            for i in range(1,4): #cycle through each type of bracket
                if character == brackets[i-1]: #{[(
                    open_brackets[i-1] += 1
                elif character == brackets[-i]: #)]}
                    open_brackets[i-1] = max(0, open_brackets[i-1] - 1) #no negative values permitted - to avoid messing with sum() check later

        if not(sum(open_brackets)): #Rule 1
            if skip: #Rule 2a
                output += '\n'
                skip = False
            if character in stopmarks:
                if nex in speechmarks: #Rule 2a
                    skip = True
                elif nex.isalpha() or nex == ' ': #Rule 2c
                    if character == '.': 
                        p = characters[i-1]
                        if p in brackets[3:]: #Rule 3d
                            output += '\n'
                        elif p.isalpha(): #Rule 3a
                            prev = characters[i] #prev word
                            j = 1
                            while characters[i-j].isalpha():
                                prev += characters[i-j].lower()
                                j += 1
                            prev = prev[::-1] #reverse it
                            if prev not in abbreviations: #Rule 3b
                                if normal_ending(prev[:-1]):  #Rule 3c
                                    output += '\n' 
                    else: #Rule 2b
                        output += '\n'
    return output        

def normal_ending(word):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    vowels = 'aeiou'
    endings = { 'a': alphabet,      #{ultimate letters of words: possible corresponding penultimate letters}
                'b': vowels + 'lmr',
                'c': 'i',
                'd': vowels + 'rdlyn',
                'e': alphabet,
                'f': vowels + 'fl',
                'g': vowels + 'ngr',
                'h': 'dhcstpagek',
                'i': alphabet,
                'j': 'andj',
                'k': vowels + 'clsrny',
                'l': vowels + 'ylwhr',
                'm': vowels + 'wlmhysr',
                'n': vowels + 'nwrgmy',
                'o': alphabet,
                'p': vowels + 'mlspy',
                'q': 'aun',
                'r': vowels + 'hr',
                's': alphabet,
                't': vowels + 'cnsplrhfx',
                'u': 'saomlernykz',
                'v': vowels + 'r',
                'w': vowels,
                'x': vowels + 'yn',
                'y': alphabet,
                'z': vowels + 'tndslz'}

    if len(word) >= 2:
        penultimate, ultimate = word[-2].lower(), word[-1].lower()
        if ultimate in endings:
            if penultimate in endings[ultimate]:
                return True
    return False















# OLD ONE - OBSCOLETE
# def split_sentences(text, max_sentence_length = 24):
#     '''
#     rule-based algorithm to find sentence boundaries
#     INPUT: large chunk of text
#     OUTPUT: text formatted so that each sentence is on a newline
#     '''
#     sentence = text.replace('<br />', ' ').replace('\n',' ').split() + [' ']*2 # ignore prior newlines & pad
    
#     line_length = 0 #keep track of the no. of words in the current line
#     for i in range(len(sentence)-2):
#         line_length += 1
#         if sentence[i][-1] in ':!?':  #!?: appended to the end of a word usually indicate the end of a sentence
#             sentence[i] += '\n' 
#             line_length = 0
#         if (sentence[i+1][0].isupper() or not sentence[i+1][0].isalpha()) and line_length > max_sentence_length:  #experimental - this detects a new sentence using capital letters alone!
#             sentence[i] += '\n'
#             line_length = 0
#         if sentence[i][-1] in '.")]>': #fullstop at end of a word may just be an abbreviation Mr. - - (which can still be at the end of a sentence)
#             if sentence[i+1][0].isupper() or not sentence[i+1][0].isalpha(): #next word starts with capital - a good sign that its a new sentence
#                 if not abbreviation(sentence[i]): #just make sure the word isnt an abbreviation - now we are sure this fullstop marks the end of a sentence
#                     sentence[i] += '\n' 
#                     line_length = 0
#                 elif line_length > 6: #this attempts to catch any abbreviations that happen to be the last word in the sentence!!!
#                     sentence[i] += '\n' 
#                     line_length = 0
#     return ' '.join(sentence)

# def abbreviation(word):
#     '''
#     Word is an abbreviation if it fulfils any one of these conditions:
#     1) a commonly known abbreviation (hon.)
#     2) single letter (C. or C) - except I
#     3) single letters followed by periods (p.m. A.A.A.)
#     4) contains no vowels nor lower case y (cf. vs. Dr.) - except occassionally for first letter (etc eg) - except its all in capitals as these are likely acronyms (CRB HP)
#     '''
#     known = 'Mr. Mrs.'.split()
#     if word in known: 
#         return True  #Rule1
#     if word == 'I': 
#         return False #Rule 2
#     l = len(word)
#     if l == 1:
#         return True #Rule 2
#     if l == 2:
#         if word[0].isalpha() and word[-1] == '.': 
#             return True #Rule 2
#     if '.' in word[:-2]: 
#         return True #Rule 3     
#     allcaps, vowely = True, False
#     if word[0].islower(): 
#         allcaps = False
#     for letter in word[1:]:
#         if letter.islower(): 
#             allcaps = False
#         if letter in 'AEIOUaeiouy': 
#             vowely = True
#     return not(allcaps or vowely) #Rule 4

#ABBREVIATION LIST
#to save the abbreviation list as a list in python - use this code:
# with open('abbreviations.txt') as f:
#     lines = f.readlines()
# print([abb.lower().strip('\n') for abb in lines[::2]])

#TESTS
#1 testing abbreviation()
# tests = 'hon. ,. A. B C. MSc PhD pm A.A.A. eg cf vs Dr etc Oz mr Mr MRI my normal word'.split()
# for test in tests:
#    print(test, "=", abbreviation(test))

#2 testing normal endings()
# test = 'hello my name is john and these are normal word endings but the following are not asdadf aggdfg'.split()
# for word in test:
#     print(word, normal_ending(word))

#3 testing split_sentences()
# sentence = '''
#     This is just a quick test! to see how well Mr. Mohammed's s.p.l.i.t.t.e.r. algorithm works... or doesnt? hehehe.
#     It also has its own new lines which may not indicate the end of
#     a sentence and thus these must be removed! can it do it? i hope so. 
#     Watch out for false fullstops. e.g. sdfsdfsd. like those. They dont indicate an end of sentence like this does. Impressive, no?
#     But the hardest, by Far, Is to detect a sentence boundary that ends with an abbreviation like this eg. Did it detect it?
#     o.k. fine.youre good.but how good.can you detect a new sentence without a fullstop to indicate it like this one here Well did it?
#     ah Easy Its Probably Just Detecting Capital Letters Like These. "thats crazy!" he said
#     narrator: 'i know.'  (also i wonder.  does it split sentences within brackets?). Now thats amazing
#     '''
# print(sentence)
# #print(split_sentences(sentence))
# print(tokenize(sentence))

#4 harder example with fused words
# with open('15609.txt') as f:
#    data = f.read()   
# #print(split_sentences(data))
# print(data)
# print()
# print(tokenize(data))