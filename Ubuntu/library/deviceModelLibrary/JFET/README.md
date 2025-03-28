# JFET (Junction field-effect transistor)

Junction Field Effect Transistor is one of the simplest types of field-effect transistor. It is opposite to the Bipolar Junction Transistor(BJT), It is a voltage-controlled devices. In JFET, the current flow is due to the majority of charge carriers, however, in BJTs, the current flow is due to both minority and majority charge carriers. Since only the majority of charge carriers are responsible for the current flow, JFETs are unidirectional.

## JFET(J204)

```
* J204 Diode model
.MODEL J204 NJF( Beta=1.004m Betatce=-.5 Rd=1  Rs=1  Lambda=3.333m Vto=-1.139 Vtotc=-2.5m Is=29.04f Isr=281.9f N=1 Nr=2 Xti=3 Alpha=698u Vk=270.4 Cgd=3.58p M=.3601 Pb=1 Fc=.5 Cgs=5.4p Kf=165E-18 Af=1 )


```


## Documentation

To know the details of J204 JFET please go through with the documentation : [J204_datasheet](https://pdf1.alldatasheet.com/datasheet-pdf/view/600341/VISHAY/J204.html)



## JFET(J2N3822)

```
* J2N3822 Diode model
.MODEL J2N3822 NJF( Beta=1.1m Betatce=-.5 Rd=1  Rs=1  Lambda=4.09m Vto=-1.962 Vtotc=-2.5m Is=181.3f Isr=1.747p N=1 Nr=2 Xti=3 Alpha=2.543u Vk=152.2 Cgd=4p M=.3114 Pb=0.5 Fc=.5 Cgs=4.627p Kf=10.2E-18 Af=1 )


```

## Documentation

To know the details of J2N3822 JFET please go through with the documentation : [J2N3822_datasheet](https://www.st.com/resource/en/datasheet/2n3700hr.pdf)


## JFET(BF244B)

```
* BF244B Diode model
.MODEL BF244B NJF( Beta=1.6m Betatce=-.5 Rd=1  Rs=1  Lambda=3.1m Vto=-2.29 Vtotc=-2.5m Is=33.57f  Isr=322.4f  N=1 Nr=2 Xti=3 Alpha=311.7u Vk=243.6  Cgd=3.35p M=.3622  Pb=1 Fc=.5 Cgs=3.736p Kf=13.56E-18 Af=1 )


```

## Documentation

To know the details of BF244B JFET please go through with the documentation : [BF244B_datasheet](https://pdf1.alldatasheet.com/datasheet-pdf/view/50801/FAIRCHILD/BF244B.html)

## Comments/Notes

Please note this is a complete Device modeling. 

## Contributer

Name: E BALAKRISHNA

Email: balakrishnaeppili0920@gmail.com

Year: 2022

Position: FOSSEE Summer Fellow 2022
