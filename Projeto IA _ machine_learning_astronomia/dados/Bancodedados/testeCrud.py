import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from EstrelarDao import (
    StarDAO, StarClusterDAO, SuperStarClusterDAO,
    GalaxyDAO, GalaxyClusterDAO, SuperGalaxyClusterDAO,
    StarDTO, StarClusterDTO, SuperStarClusterDTO,
    GalaxyDTO, GalaxyClusterDTO, SuperGalaxyClusterDTO
)


def testar_star():
    print("\n--- [1/6] TESTANDO CRUD: Star ---")
    dao = StarDAO()
    
    nova = StarDTO(
        idStar=None,
        nameStar="Betelgeuse",
        spectralClass="M1-M2",
        mainSpectralClass="M",
        evolutionaryStage="Supergigante Vermelha",
        distanceStar_LY=642.5,
        temperatureStar_K=3500.0,
        luminosityStar_logSun=4.7,
        radiusStar_logSun=2.9,
        massStar_logSun=1.2
    )
    id_criado = dao.save(nova)
    print(f"[CREATE] Estrela inserida com ID: {id_criado}")

    buscada = dao.find_by_id(id_criado)
    print(f"[READ] Encontrada: {buscada.nameStar} (Temperatura: {buscada.temperatureStar_K}K)")

    buscada.temperatureStar_K = 3600.0
    dao.update(buscada)
    atualizada = dao.find_by_id(id_criado)
    print(f"[UPDATE] Temperatura atualizada: {atualizada.temperatureStar_K}K")

    dao.delete(id_criado)
    removida = dao.find_by_id(id_criado)
    print(f"[DELETE] Removida com sucesso? {removida is None}")


def testar_star_cluster():
    print("\n--- [2/6] TESTANDO CRUD: StarCluster ---")
    dao = StarClusterDAO()
    
    novo = StarClusterDTO(
        idStarCluster=None,
        nameStarCluster="Pleiades",
        typeStarCluster="Aglomerado Aberto",
        distanceStarCluster_LY=444.2,
        ageStarCluster_GYL=0.1,
        estimatedStarsCountStarCluster=1000.0,
        coreRadius_PC=1.5,
        tidalRadius_PC=5.8,
        massStarCluster_logSun=2.9
    )
    id_criado = dao.save(novo)
    print(f"[CREATE] Aglomerado Estelar inserido com ID: {id_criado}")

    buscado = dao.find_by_id(id_criado)
    print(f"[READ] Encontrado: {buscado.nameStarCluster}")

    buscado.ageStarCluster_GYL = 0.12
    dao.update(buscado)
    atualizado = dao.find_by_id(id_criado)
    print(f"[UPDATE] Idade atualizada: {atualizado.ageStarCluster_GYL} GYL")

    dao.delete(id_criado)
    removido = dao.find_by_id(id_criado)
    print(f"[DELETE] Removido com sucesso? {removido is None}")


def testar_super_star_cluster():
    print("\n--- [3/6] TESTANDO CRUD: SuperStarCluster ---")
    dao = SuperStarClusterDAO()
    
    novo = SuperStarClusterDTO(
        idSuperStarCluster=None,
        nameSuperStarCluster="Westerlund 1",
        hostGalaxySuperStarCluster="Via Lactea",
        effectiveRadiusSuperStarCluster_pc=1.0,
        ageSuperStarCluster_myr=4.0,
        totalMassSuperStarCluster_logSun=4.8,
        starFormationRateSuperStarCluster_sun_y=0.05,
        centralDensitySuperStarCluster_M_sun_pc3=100000.0,
        luminositySuperStarCluster_logSun=6.2
    )
    id_criado = dao.save(novo)
    print(f"[CREATE] Super Aglomerado Estelar inserido com ID: {id_criado}")

    buscado = dao.find_by_id(id_criado)
    print(f"[READ] Encontrado: {buscado.nameSuperStarCluster}")

    buscado.ageSuperStarCluster_myr = 4.5
    dao.update(buscado)
    atualizado = dao.find_by_id(id_criado)
    print(f"[UPDATE] Idade atualizada: {atualizado.ageSuperStarCluster_myr} Myr")

    dao.delete(id_criado)
    removido = dao.find_by_id(id_criado)
    print(f"[DELETE] Removido com sucesso? {removido is None}")


def testar_galaxy():
    print("\n--- [4/6] TESTANDO CRUD: Galaxy ---")
    dao = GalaxyDAO()
    
    nova = GalaxyDTO(
        idGalaxy=None,
        nameGalaxy="Andromeda",
        hubbleTypeGalaxy="SA(s)b",
        generalMorphologyGalaxy="Espiral",
        distanceGalaxy_LY=2537000.0,
        effectiveRadiusGalaxy_KPC=7.0,
        luminosityGalaxy_logSun=10.4,
        starFormationRateGalaxy_Sun_Y=1.0
    )
    id_criado = dao.save(nova)
    print(f"[CREATE] Galáxia inserida com ID: {id_criado}")

    buscada = dao.find_by_id(id_criado)
    print(f"[READ] Encontrada: {buscada.nameGalaxy} ({buscada.generalMorphologyGalaxy})")

    buscada.starFormationRateGalaxy_Sun_Y = 1.2
    dao.update(buscada)
    atualizada = dao.find_by_id(id_criado)
    print(f"[UPDATE] Taxa de formação estelar: {atualizada.starFormationRateGalaxy_Sun_Y}")

    dao.delete(id_criado)
    removida = dao.find_by_id(id_criado)
    print(f"[DELETE] Removida com sucesso? {removida is None}")


def testar_galaxy_cluster():
    print("\n--- [5/6] TESTANDO CRUD: GalaxyCluster ---")
    dao = GalaxyClusterDAO()
    
    novo = GalaxyClusterDTO(
        idGalaxyCluster=None,
        nameGalaxyCluster="Virgo Cluster",
        morphologyTypeGalaxyCluster="Irregular",
        distanceGalaxyCluster_LY="53800000.0",
        redShiftGalaxyCluster_z=0.0036,
        memberGalaxiesCountGalaxyCluster=1500.0,
        virialRadius_Mpc=2.2,
        totalMassGalaxyCluster_logSun=14.5,
        IntraclusterGasTemp_keV=2.3,
        xRayLuminosity_erg_s=1e43
    )
    id_criado = dao.save(novo)
    print(f"[CREATE] Aglomerado de Galáxias inserido com ID: {id_criado}")

    buscado = dao.find_by_id(id_criado)
    print(f"[READ] Encontrado: {buscado.nameGalaxyCluster}")

    buscado.redShiftGalaxyCluster_z = 0.0038
    dao.update(buscado)
    atualizado = dao.find_by_id(id_criado)
    print(f"[UPDATE] Redshift atualizado: {atualizado.redShiftGalaxyCluster_z}")

    dao.delete(id_criado)
    removido = dao.find_by_id(id_criado)
    print(f"[DELETE] Removido com sucesso? {removido is None}")


def testar_super_galaxy_cluster():
    print("\n--- [6/6] TESTANDO CRUD: SuperGalaxyCluster ---")
    dao = SuperGalaxyClusterDAO()
    
    novo = SuperGalaxyClusterDTO(
        idSuperGalaxyCluster=None,
        nameSuperGalaxyCluster="Laniakea",
        cosmicStructureTypeSuperGalaxyCluster="Superaglomerado de Galáxias",
        distanceSuperGalaxyCluster_Mpc=160.0,
        redshiftSuperGalaxyCluster_z=0.037,
        memberClustersCount=300.0,
        extentLength_Mpc=160.0,
        totalMassGalaxyCluster_logSun=15.0,
        overdensityFactor=2.5
    )
    id_criado = dao.save(novo)
    print(f"[CREATE] Super Aglomerado de Galáxias inserido com ID: {id_criado}")

    buscado = dao.find_by_id(id_criado)
    print(f"[READ] Encontrado: {buscado.nameSuperGalaxyCluster}")

    buscado.overdensityFactor = 2.8
    dao.update(buscado)
    atualizado = dao.find_by_id(id_criado)
    print(f"[UPDATE] Fator de sobredensidade: {atualizado.overdensityFactor}")

    dao.delete(id_criado)
    removido = dao.find_by_id(id_criado)
    print(f"[DELETE] Removido com sucesso? {removido is None}")


def main():
    print("=" * 60)
    print("      INICIANDO TESTE INTEGRADO DO DAO ASTRONÓMICO")
    print("=" * 60)
    
    try:
        testar_star()
        testar_star_cluster()
        testar_super_star_cluster()
        testar_galaxy()
        testar_galaxy_cluster()
        testar_super_galaxy_cluster()
        
        print("\n" + "=" * 60)
        print("    TODOS OS TESTES CRUD FORAM EXECUTADOS COM SUCESSO! 🎉")
        print("=" * 60)
    except Exception as e:
        print(f"\n[ERRO DURANTE A EXECUÇÃO DOS TESTES]: {e}")


if __name__ == "__main__":
    main()