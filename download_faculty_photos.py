#!/usr/bin/env python3
"""
Download all GCETTS faculty photos into ./assets/faculty/
Run from your repo root:   python3 download_faculty_photos.py
Re-run any time to refresh. Already-downloaded files are skipped.
"""
import os, sys, urllib.request

OUT = os.path.join("assets", "faculty")
PHOTOS = {
    "cse-dipak-kumar-kole.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUAf4pvUsY92DYL5nDxiSW_3uyGAD5UlGitXmZ1C32GHlnOEiSdyuqQesfc6GvE8cYI6dQwBnauB1GwuUlDa0FER2nSEKXjBLmirmiYbu77muKU5wFQE-NmjxEMHhKnWq6VTdthHr0H5xOJkyBmZcOZt4zpqXSh61SsM3gJnkHDGVTO1iz7_hbCvaRkaw_ILsXKqb5DBTWrLSu5S84uFbJyfCtgjOEtNRU5gqwn5=w1280",
    "cse-krishan-kundu.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUAFZy2l51N_SUV7tBXwuQ9Lo2noZrnoeSOCZOSjFxE5NguJHj2u32SHAZgNOsiSt_SflqzjXSC9BGrSB6UuSvrgCtsOrOGl4aetIbggVej6UEcLvEr45p_wDFYUELUCb0VDpdcHTqtJtNZhDb901icaTlvXfCs__Pek9vv4oQ8_iSiNugBJThGKYAc5LDpUHUJdvA7gMrscg_d5jzNJyUXmmUVIR06fPv3U8ViC=w1280",
    "cse-manik-mondal.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUCO4_5F7dinyWUxj7y-nsSCe9StLEz9xUcNlG9Fv9UVQB39mqHzhzmiaEWG_xet-guE0sxWUNjDN1fFGXgZzAcS89MaDQ4nGXfG7F132oDSowXissLhqEQq71CVqgIHHmM0N7_gihAdnGpXVktQXtHwmAo42ahSu9QE08JmsEcAcw0rEMQ4tKbhSpxs7Ef9yyxMJap5C28duzP3TEBh4oRACPv4-plA92qlIrvmvLk=w1280",
    "cse-manjari-saha.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUD6nOmWQgfOwM2VUNU1OG2jRFWiwqpJEGDN6WPRKCNBvfrtu7VCwS3OZUKIpcMVkVWSAMyWGyrUyv88HePH1fyf7TlL8bEc0LkFQBDuRn7O2OyWFfqfyrEKqKdxq-RmS7Tz7kckYysru5_AgcIQyC1sMa5voWjSOwCnUB43E2ecU-zHDci_OKxHmJQkCozj-UYX4771O1gP2BUD0LC4ddSIzPtdR7cEmRpb_5qb4_M=w1280",
    "cse-prasanta-mandal.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUDfkxjsl97GpRd9ca3dY_UWhQfVQhcAoKX4qIaggmwFoJw34zEwldMuAMjzA4n7jp-lP57CxK5Bd0bM8MJT5s5C5VW6AEL6ViegrkFj9jtdSB0PVVDQx93RcsnNrOFzsuDN88-5ctjJUtQ31yoQLq2kcskbFI2qPc_dgl5U6C4FMhY9F5enICeJg9jTZUskaUb4t0CrRN7XKttSDmgRu_gym9cXUqmEOZR_bXgy=w1280",
    "cse-preetam-kumar-sur.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUAOD0uUxDrg4642559qdLUwZz2eQTCC-0q6mIRXCanRQNvn9ucwTnYpJPiw_BumgNlu27abiOD7J2OX9ZbbgIo6ulO9UkPZukYmgpcYatjXBBx8Ql6LRNAoyct5lLrCDwAnmZl_QnOGQap_qcNFaptTUqYlSPhIhkP1fOhi3SzAxO7Cxl8Am164fzPUd5_ecsmAL9d1ASxz5VDiqIdSKZKV5noSnpoaKZL2x5q6=w1280",
    "cse-sourav-de.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUC6Y3NbUjSRutfJ2sLyGgh42xjxkqFN4lAnOX3R7La5aAFNuNOFUn_FjyO7eIhRKoThnPtdNjSJS3qk55-leb0WaCWRNzSggh0Za0Gog24sGFCjO-CycKKhS7yMSC9ConrI_l-hBKd_bCyjCUxwJEyTqxP66T_thog5PkKcUsG0CXiD88v33MO38DUvDr_IO_e0W1NvGOrYs8UMIfuBIR6iVN5KIKibqlg2PZc-xNM=w1280",
    "it-biswajit-sanyal.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUAcr9lemaQO-h0Qx4d9G30yV0TroE46hgJymUsIK0_q03oPMA29j-LDBBSntGj_qvATwPtFxd82JaOhBj3asq10h9hV1BUINDn-XSvKZGzHKIOMK9e1xcCq1ZBB-df9rDyrWpPj6lhzoatmpZX3SAPujhaB24nzSDzemisxBNLXMkNF7U4z0vw2S1-QT7IJp_0jhhruN9uoMiIuvJ11dLWGPO7JqdJVZZATanuHkE8=w1280",
    "it-pijush-kanti-kumar.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUC69Dy3FNyrw2HncwQPipW5KnDiHQa9MtWfecnbDPU3MVvtayc7ZB51XHaTRCgQXhxLHf1qypIytbKc5VENYsVyhoYsAvLvuw5y4sAK6q5LoyScx2dgLYW3JJp3AfbP1BCmAnTuieqk-W2RanZwJjwb5nwOPY8dX9tFHVp6BinbKjYO115waoZyPBAgsiiklx7O_UtF76ztJv9lDyj7XsPnWynFeuroqqeLW3y6Zdg=w1280",
    "it-pranay-adak.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUBNzLwirpEaPOwFXN_da8WSYwKF5GhmHej0KAty4P4u-eobuO4HDbwLwNVGH1E8eXTdz0fXTECB8QcUAGVwnmVGMfN2UY4kTdxvxPL9b1XY_UdR5IzWaIhSoXOeljP9CGCIA4tDAF6t8sVk6qZVWugrtGXz6tFtr3EwDSAhooYgLoAUGy5Hi0hCdjMzVUCmbB30pR4skLJjIWpWluZjbToroi7lH8O-csWwMo4Zps4=w1280",
    "it-sima-ghosh.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUCQHq5cwWZ-hbY02kJqebdK2epBY77PLWpfDf29WUG1JzJfxrpkbXfh-cDlpWTnGV0sLTHFFVXOrkKinkuyHSAtNYOBsTOT5J39RVhfzSXMyjlRA9kmT0v46DfZTvIZKxrIret2OHE0_vYtQk_RcdwfdDQ_dZ2Qr9wSeD_xcsPE3Pw5jvuHNT181ulBxUlrz7d_9PV2Gcux6T4ho2bUNJ06kLmmDjiz2ZfIYI6N=w1280",
    "it-tapan-mandal.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUDulnwClsmopmeBozbEYi54C088QEXQ5MsL3FbI7UIgAnpiAKJn0AADQCIoQqNIGUWq2zkkKC6LMf4M2ON50gQRbuNe-m4XApsCDwY3AIwLA4nk3CTVtLgsJqXy-GUvJ9bu6Na45_VWVDZUFUc-74At9EPluHYPh-IZi6qNjFPdAyh5j-WOIbvLMD59UlZrSZHWbRH8ogc6X2Z17X8iDZgrF9sccvejLn-tZAXFbKM=w1280",
    "tt-adwaita-konar.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUBPFSlmbrRtUiNxwIsfPL248aCMl3OQbdEcUP0Of-Io8zksRD_-Qk37H2ST1Zg9SxK0zdqxhRkDcP8YskdQAkHt7TbsvsQIV77peozuYwMKg6aVPtqBwTyeSyI_KjobNPcmN7_P9eX1BKCSyEMe_Jhni0djLWL00VGKo_-tTF-mwgnhI4WITrs3tnrWIjljGCENVxOHJBz_JVlZqiOzcFdyWKaxA4CvWYkkQpiP0C0=w1280",
    "tt-arijit-chakraborty.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUC9gWBe8RGg5lkO9e9loq3bYxdpSrFPRJd2ZLn18LwUym7VR1ANNaITlI8xargSiV1SLPL_x8jI4im_GzKbjim5sfLPxIaPscfkzsCHbvvxAnfXKOU8aDYQAJd6RA4FkHy2_IgRRnEbzpwRzkOYn0Z0zoz7Ki9_CuiM9zgrPthcVTao_SJ97fupp3gWzd1pP18ZCVqKgYSiQ9QRb--7KAWTDkmtjwRD6Wib74-V=w1280",
    "tt-sudipta-sekhar-mahish.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUCpGiurjOXZgkK7Jk5w9dbXBDTHeJ0uOgyF7zyJAZnjpWa-7konDG9ErfN9rN4fo99O0sABwceE2I3qt_k4CIiyr225CQXDhR2c8wI-B6A9I6fpfukaWOr2vxRRplLT-HDDy5kBGLRqsMWY_o4tvJpUDo0B-Z8aBWVXFwd1L96PJsUsaI6hrD1ntSWzaLEQ15fvfHTrxNiIUxEJmbpSmwS6-cTefoa0SzX2AH78BqY=w1280",
    "tt-suchibrata-ray.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUApr-STenCrLCWpkABewAQUjQqylyc22R9H_ckRI6XpQKIkKGqLn1kk9y6Kfb7CdrKtdU2Dp-bPWsY-hZ2YJTpMUfpnT7LH7ANTQefiogJ7k2UN5ARcUubmM40R3qirztzIOcgan-JyCebnKVAPTkGN5M-1jlaZihA2QRQt3K2U1RdYONKLorSwUWyzNDJQ11oN6HFIsz3diuaV20099jNcXKFumMx_OtqLVKsx7xA=w1280",
    "tt-anirban-dutta.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUCLGwQwhCsfLdrGICgvxsJaRixv0nUl7HJAIq8eqtZghp6nTjily1ol3gNAwyYUvWbnkrOWv_CaanSL2o24ifWpMX9Wx6KODUlB2hpXH2usiGVHjY9Cvpjh0j0DSBTU9R4zAJmyM0TmSEldJ0Ki2xZnmd6Yf1AiXatwypCtoHQ8hdbYl4MY5-MrekAArBYhbsBVga8grc04yi-wPzT8MrXiUznQJ2p1qx2iijXk=w1280",
    "tt-aranya-mallick.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUDO_sMHgnA-TOMsthAcH47JxZOEr2XHPRKGZ1y6nM9fbJGVyYshxIZulwS236YmViOjwXTgYVGbe2Hnj53u1euWGLRf63OPB25cI8kZjmjXynsr6Jh--quSX-5poeyWFNx2_71O6BonBuO2ehxskDcCL_oramW4RQaGXQkXkw2FCza1hU0laEQ5N0CXLZxpWstg8512tVJSUWOu6ER18qXZ-7IuS3wDl7eRYG-xUBA=w1280",
    "tt-mallika-datta.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUD3XPqPxykXuGzGo8GfU8RWgmSjSwxoghIZo_MRbwSgNjeLnzFCUDloNNlChiGGrJnUu9cMegFko7nkoMNW55S60kb0r3h3Y0Ei8JA25v979YTaTX0rtcnCivKpmXwBrn9WWQHg4Y8MLAToDLzHwIeLOAN0mWcDVJrqWpDh-flIDB3SewbHemL3mhs4ADWar9jfwMUpggikDd5wpxOB6vekHF_Hj2sdA8XNnKFM=w1280",
    "tt-md-samsu-alam.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUB-S-1qtelfap1aMHEX3SKbf20ssHuVTLN_zC8Dh8lLA1-JpT_m9Xbw3ClZerwNElzT5h16joujE48qfE8kgQmELCjCtpJdwt2ymj5sROyDN-R1p-BnaFTH5r3q1P03NutAU4Xp-fCK527wE6iWpz3W2K97pXBOhrjuPyGMQEaYOriwyTE1WYztmTFp8gvZ-8ZMPa7unSYLyDv3AGxT2QXiDfGspSJv_QFrCEiqecw=w1280",
    "tt-sajal-barman.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUAwnV7zxs_Yh5hqetPmKl0enhSIcIABtPCjpAYFC0sXctdb3Ev2qKNiiixWuLkpJ4dmtbJVz4oGlOnKs75MeA49R4iisrc4dylkcwr6ssd1WVAlU1Sr7LzZp63NvBQ_9ggfsvL-k0A5_Fcm2wRmudti7-lFbI1VC6I-5L3z-oMr3TE1tQWmnw284aV1z8q6peFSLeUyyS6XrVG2v1uA_kH6L16G_v9fnm01ow=w1280",
    "tt-susanta-sekhar-de.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUDT1X79pGCP4iFfgihdvlWjCb_AQeGFG2xA5FnroMDLviQJHl5CPbhRZhmApBd9dnm3-CTbHjXqwLTFNhREsb9sbtDdNMQhkDBn3aBDhqTBhXak-6g8R8B2r_vmeCNNfDe3_Hd7fEfu0u20Xl0AqoI8eUJMk7tR-uzxq3Y_sBAsg8h_l9Jdfy9g1xF_ghDCRpIE1Z-BjP_KfZUjH-X3xvGqqJxn1zVQ183AQEJF=w1280",
    "be-dipankar-chatterjee.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUAWaPXctLvf6upjWHqY3PBHfG6C-zvrTH0bVMJ9F6xhSpXB2zY8jKynuhl7yoGiEENTmSq6SCM0X428Uh4hjYFicAvSOeBxItfI9vZdmbl9_o9xn9O_jxephGjdYFhlpR5Ewi3QzUi-PwM2YmiGjC3zSE-LyoZcKy-dZlMXkN7yYjK9ypMj7KGS1PekP_VOXCJ41SSK5sUptXFjrbKm-ByT_TWfy6iP6D4Ie-o1hWA=w1280",
    "be-priyajit-mukherjee.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUBErLoHADJ6W3gw7XdDzqxKPX0UDOd92EronDOE4py_arB2v9EU3OBqqD3SOlz9F1BWYI02S7T78XzTM31x27hJ8-7dJoDycuN9YyEmB4ShaKVTRA6sZ0RhfHHOfl-W8XdzWUhWuab1zBJCOef2L8KVKV5fwitelYKD5O5kceVFLJgRIliZRCwH7bLMoJXdjOzZ54iQBkiSgrLAVKI-nUcmn_o-bGcIPEsnz2o_=w1280",
    "be-tripuresh-deb-singha.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUAZ5VccMNacQdk5Jmx6tZf9It3FUy31Et2gmigKiGd7_vzzJhaAu4U02GIzVDm3oDh68GzkgzlGCJEFK4P90FFEulirs0kXYFrNdRZpLPJf5TbQJPf3cblHj2x01rZCh3wKK6YXs6VahTdB0tZe4q8jETdnHKuzGp0P0WSciGOSmgCT9gB1fPK2qoNhZQrdxe6mdjuKM9wJKcCmcLT2JHDrhOUK5sXdjzWYEO-F9s8=w1280",
    "bs-arnab-kumar-de.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUC0dRg_hok5V17eEDZMgFsPllzAASN1evlrGYGd78N6nsIaqb_ETe6wRWU8Md7oqjhd1RXyJuB0n3fdTglfB-EhPNaBrVh_dkQ5VeT-AkzKJ0eccOrxtNUkY91l9O4ktoAKQaNsQ5EF1juBnXAI0Uz7xA3C_AKlwvo3vd7BximQg68KrRvgDBcOCtMfmen-L-ixfxa7WalMbGu99tamXwuAc448x92HP8dBVD3r5tw=w1280",
    "bs-dilip-maji.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUAevY47q-yg1aJ5pTueRQBQ0Hm7iulJstOzXmErOiY4tYP0CzJ5RUaqaGYUOoxiQYpgkCTzUGjq3KytgohhXXdyTTpAhj8eSIBrYOqTvtVE0WAvInNCcXoXV4r-6YGX2n4qaeXbyPK_bhoHbwPd8B_JCja8ojm19PBxlRyq4-T3u8fO49oRW581rryy_e-nWFNn_qvUZKjniZQ93lF2qop8pQyMfQD2X3B_NBMQoXg=w1280",
    "bs-prabir-kumar-mukherjee.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUDKOMSgAHwxzuwNcJur5SXcqyW_A_zF3uafh2xaMTWGVD0kwTz5GrcoHExaJMikWRQOMUtNng1yIrKPebjQtkIExaG7HqR-R2vWN8weVAaR0r_I_ZvMvTqibsQq7Mb7piP-eKmvqJ2rI0NKZTmYMubCFmV8cvvuXfjYuvQ2x9TjrxnG3yiF1jZEpDF8iBg8f8iMIyyMOj3Lbv2GWk3TUi_jYoVCdVr3ovYxr-oHqjY=w1280",
    "bs-seemantini-chattopadhyay.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUAsS7bXDoiTLL_tfJhh6Foo-9QzCR2WvDPTDdyygV7A94Z-9gZvxMcaIxcenO5K_7yYT_RGo4vA45ytKQ8DM4wk3AB3kAjweiBGA9CTxmOgYgnpiwFj2Lk9fRTHOksj_WVfvSazlWKo6FT_aLhGEApAANq86jMg9AUgqETIb71wzxJ7h40K8glSKf3xLO3catisoMWATqzkZIzNvhrZrb3tjQrcOAJRHTvHV_Zg=w1280",
    "lib-ananda-majumdar.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUDYJwk5PMKpNCPj_6nn-TueL8RjCvy_k_k8EO9IbdwC6iG_y_ZJWSWh6qNl5UXr4ODuV35HFcYNYGVM-NtzVuYyi2l6ZtFw0AieXdGbdxpu8KmH4nFwE10dpMczg9D7GRCSuH1WxJlqOldfoz3JWNgLO6sZNvbffucRvvF1Wp74ZA4VG9iXw3CADpBxjh7z--uWKSRN3pOJLOPiou3mNupmsGKx2Mnl1pVjvP6aNyc=w1280"
}

def main():
    os.makedirs(OUT, exist_ok=True)
    ok = skip = fail = 0
    for fname, url in PHOTOS.items():
        dest = os.path.join(OUT, fname)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            skip += 1; continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as out:
                out.write(r.read())
            print("  saved", fname); ok += 1
        except Exception as e:
            print("  FAILED", fname, "->", e); fail += 1
    print(f"\nDone. {ok} downloaded, {skip} skipped, {fail} failed -> {OUT}/")
    if fail:
        print("If some failed, the page falls back to the live URL, then to initials.")

if __name__ == "__main__":
    main()
