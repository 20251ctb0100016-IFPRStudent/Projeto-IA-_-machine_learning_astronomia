import sqlite3
import os
from dataclasses import dataclass
from typing import Optional, List


# ==========================================
# 1. DATA TRANSFER OBJECTS (DTOs)
# ==========================================

@dataclass
class StarDTO:
    nameStar: str
    spectralClass: str
    mainSpectralClass: str
    evolutionaryStage: str
    distanceStar_LY: float
    temperatureStar_K: float
    luminosityStar_logSun: float
    radiusStar_logSun: float
    massStar_logSun: float
    idStar: Optional[int] = None
    idStarCluster: Optional[int] = None

@dataclass
class StarClusterDTO:
    nameStarCluster: str
    typeStarCluster: str
    distanceStarCluster_LY: float
    ageStarCluster_Gyr: float
    estimatedStarsCountStarCluster: int
    coreRadius_PC: float
    tidalRadius_PC: float
    massStarCluster_logSun: float
    idStarCluster: Optional[int] = None
    idGalaxy: Optional[int] = None

@dataclass
class SuperStarClusterDTO:
    nameSuperStarCluster: str
    hostGalaxySuperStarCluster: str
    effectiveRadiusSuperStarCluster_pc: float
    ageSuperStarCluster_myr: float
    totalMassSuperStarCluster_logSun: float
    starFormationRateSuperStarCluster_sun_y: float
    centralDensitySuperStarCluster_M_sun_pc3: float
    luminositySuperStarCluster_logSun: float
    idSuperStarCluster: Optional[int] = None
    idGalaxy: Optional[int] = None

@dataclass
class GalaxyDTO:
    nameGalaxy: str
    hubbleTypeGalaxy: str
    generalMorphologyGalaxy: str
    distanceGalaxy_LY: float
    effectiveRadiusGalaxy_KPC: float
    luminosityGalaxy_logSun: float
    starFormationRateGalaxy_Sun_Y: float
    idGalaxy: Optional[int] = None
    idGalaxyCluster: Optional[int] = None

@dataclass
class GalaxyClusterDTO:
    nameGalaxyCluster: str
    morphologyTypeGalaxyCluster: str
    distanceGalaxyCluster_LY: float
    redShiftGalaxyCluster_z: float
    memberGalaxiesCountGalaxyCluster: int
    virialRadius_Mpc: float
    totalMassGalaxyCluster_logSun: float
    IntraclusterGasTemp_keV: float
    xRayLuminosity_erg_s: float
    idgalaxyCluster: Optional[int] = None
    idSuperGalaxyCluster: Optional[int] = None

@dataclass
class SuperGalaxyClusterDTO:
    nameSuperGalaxyCluster: str
    cosmicStructureTypeSuperGalaxyCluster: str
    distanceSuperGalaxyCluster_Mpc: float
    redshiftSuperGalaxyCluster_z: float
    memberClustersCount: int
    extentLength_Mpc: float
    totalMassGalaxyCluster_logSun: float
    overdensityFactor: float
    idSuperGalaxyCluster: Optional[int] = None


# ==========================================
# 2. DATA ACCESS OBJECTS (DAOs)
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "DadosAstronomico.sqlite")

class BaseDAO: # ou no __init__ do seu DAO
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

# ----------------------------------------------------------------------------------------------------- Estrelas -----------------------------------------------------------------------
class StarDAO(BaseDAO):
    def find_by_id(self, star_id: int) -> Optional[StarDTO]:
        query = """
        SELECT idStar, nameStar, spectralClass, mainSpectralClass, evolutionaryStage,
               distanceStar_LY, temperatureStar_K, luminosityStar_logSun,
               radiusStar_logSun, massStar_logSun, idStarCluster
        FROM star WHERE idStar = ?
        """
        with self._get_connection() as conn:
            row = conn.execute(query, (star_id,)).fetchone()
            if row:
                return StarDTO(
                    idStar=row[0], nameStar=row[1], spectralClass=row[2],
                    mainSpectralClass=row[3], evolutionaryStage=row[4],
                    distanceStar_LY=row[5], temperatureStar_K=row[6],
                    luminosityStar_logSun=row[7], radiusStar_logSun=row[8],
                    massStar_logSun=row[9], idStarCluster=row[10]
                )
        return None

    def save(self, star: StarDTO) -> int:
        query = """
        INSERT INTO star (
            idStar, nameStar, spectralClass, mainSpectralClass, evolutionaryStage,
            distanceStar_LY, temperatureStar_K, luminosityStar_logSun,
            radiusStar_logSun, massStar_logSun, idStarCluster
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(idStar) DO UPDATE SET
            nameStar=excluded.nameStar, spectralClass=excluded.spectralClass,
            mainSpectralClass=excluded.mainSpectralClass, evolutionaryStage=excluded.evolutionaryStage,
            distanceStar_LY=excluded.distanceStar_LY, temperatureStar_K=excluded.temperatureStar_K,
            luminosityStar_logSun=excluded.luminosityStar_logSun, radiusStar_logSun=excluded.radiusStar_logSun,
            massStar_logSun=excluded.massStar_logSun, idStarCluster=excluded.idStarCluster
        """
        with self._get_connection() as conn:
            cursor = conn.execute(query, (
                star.idStar, star.nameStar, star.spectralClass, star.mainSpectralClass,
                star.evolutionaryStage, star.distanceStar_LY, star.temperatureStar_K,
                star.luminosityStar_logSun, star.radiusStar_logSun, star.massStar_logSun, star.idStarCluster
            ))
            conn.commit()
            return cursor.lastrowid

    def find_all(self, limit: int = 100) -> List[StarDTO]:
        query = """
        SELECT idStar, nameStar, spectralClass, mainSpectralClass, evolutionaryStage,
               distanceStar_LY, temperatureStar_K, luminosityStar_logSun,
               radiusStar_logSun, massStar_logSun, idStarCluster
        FROM star LIMIT ?
        """
        estrelas = []
        with self._get_connection() as conn:
            rows = conn.execute(query, (limit,)).fetchall()
            for row in rows:
                estrelas.append(StarDTO(
                    idStar=row[0], nameStar=row[1], spectralClass=row[2],
                    mainSpectralClass=row[3], evolutionaryStage=row[4],
                    distanceStar_LY=row[5], temperatureStar_K=row[6],
                    luminosityStar_logSun=row[7], radiusStar_logSun=row[8],
                    massStar_logSun=row[9], idStarCluster=row[10]
                ))
        return estrelas

        def delete(self, id_star: int) -> bool:
            query = "DELETE FROM star WHERE idStar = ?"
            with self._get_connection() as conn:
                cursor = conn.execute(query, (id_star,))
                conn.commit()
                return cursor.rowcount > 0
# ---------------------------------------------------------------------------------------- Aglomerado Estrelar ---------------------------------------------------------------------------
class StarClusterDAO(BaseDAO):
    def find_by_id(self, cluster_id: int) -> Optional[StarClusterDTO]:
        query = """
        SELECT idStarCluster, nameStarCluster, typeStarCluster, distanceStarCluster_LY,
               ageStarCluster_Gyr, estimatedStarsCountStarCluster, coreRadius_PC,
               tidalRadius_PC, massStarCluster_logSun, idGalaxy
        FROM starCluster WHERE idStarCluster = ?
        """
        with self._get_connection() as conn:
            row = conn.execute(query, (cluster_id,)).fetchone()
            if row:
                return StarClusterDTO(
                    idStarCluster=row[0], nameStarCluster=row[1], typeStarCluster=row[2],
                    distanceStarCluster_LY=row[3], ageStarCluster_Gyr=row[4],
                    estimatedStarsCountStarCluster=row[5], coreRadius_PC=row[6],
                    tidalRadius_PC=row[7], massStarCluster_logSun=row[8], idGalaxy=row[9]
                )
        return None

    def save(self, cluster: StarClusterDTO) -> int:
        query = """
        INSERT INTO starCluster (
            idStarCluster, nameStarCluster, typeStarCluster, distanceStarCluster_LY,
            ageStarCluster_Gyr, estimatedStarsCountStarCluster, coreRadius_PC,
            tidalRadius_PC, massStarCluster_logSun, idGalaxy
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(idStarCluster) DO UPDATE SET
            nameStarCluster=excluded.nameStarCluster, typeStarCluster=excluded.typeStarCluster,
            distanceStarCluster_LY=excluded.distanceStarCluster_LY, ageStarCluster_Gyr=excluded.ageStarCluster_Gyr,
            estimatedStarsCountStarCluster=excluded.estimatedStarsCountStarCluster, coreRadius_PC=excluded.coreRadius_PC,
            tidalRadius_PC=excluded.tidalRadius_PC, massStarCluster_logSun=excluded.massStarCluster_logSun,
            idGalaxy=excluded.idGalaxy
        """
        with self._get_connection() as conn:
            cursor = conn.execute(query, (
                cluster.idStarCluster, cluster.nameStarCluster, cluster.typeStarCluster,
                cluster.distanceStarCluster_LY, cluster.ageStarCluster_Gyr,
                cluster.estimatedStarsCountStarCluster, cluster.coreRadius_PC,
                cluster.tidalRadius_PC, cluster.massStarCluster_logSun, cluster.idGalaxy
            ))
            conn.commit()
            return cursor.lastrowid

    def find_all(self, limit: int = 100) -> List[StarClusterDTO]:
        query = """
        SELECT idStarCluster, nameStarCluster, typeStarCluster, distanceStarCluster_LY,
               ageStarCluster_Gyr, estimatedStarsCountStarCluster, coreRadius_PC,
               tidalRadius_PC, massStarCluster_logSun, idGalaxy
        FROM starCluster LIMIT ?
        """
        aglomerados = []
        with self._get_connection() as conn:
            rows = conn.execute(query, (limit,)).fetchall()
            for row in rows:
                aglomerados.append(StarClusterDTO(
                    idStarCluster=row[0], nameStarCluster=row[1], typeStarCluster=row[2],
                    distanceStarCluster_LY=row[3], ageStarCluster_Gyr=row[4],
                    estimatedStarsCountStarCluster=row[5], coreRadius_PC=row[6],
                    tidalRadius_PC=row[7], massStarCluster_logSun=row[8], idGalaxy=row[9]
                ))
        return aglomerados

    def delete(self, cluster_id: int) -> bool:
                query = "DELETE FROM starCluster WHERE idStarCluster = ?"
                with self._get_connection() as conn:
                    cursor = conn.execute(query, (cluster_id,))
                    conn.commit()
                    return cursor.rowcount > 0
# --------------------------------------------------------------------------------------- SuperAglomeradoEstrelar ----------------------------------------------------------------------------
class SuperStarClusterDAO(BaseDAO):
    def find_by_id(self, s_cluster_id: int) -> Optional[SuperStarClusterDTO]:
        query = """
        SELECT idSuperStarCluster, nameSuperStarCluster, hostGalaxySuperStarCluster,
               effectiveRadiusSuperStarCluster_pc, ageSuperStarCluster_myr,
               totalMassSuperStarCluster_logSun, starFormationRateSuperStarCluster_sun_y,
               centralDensitySuperStarCluster_M_sun_pc3, luminositySuperStarCluster_logSun, idGalaxy
        FROM superStarCluster WHERE idSuperStarCluster = ?
        """
        with self._get_connection() as conn:
            row = conn.execute(query, (s_cluster_id,)).fetchone()
            if row:
                return SuperStarClusterDTO(
                    idSuperStarCluster=row[0], nameSuperStarCluster=row[1],
                    hostGalaxySuperStarCluster=row[2], effectiveRadiusSuperStarCluster_pc=row[3],
                    ageSuperStarCluster_myr=row[4], totalMassSuperStarCluster_logSun=row[5],
                    starFormationRateSuperStarCluster_sun_y=row[6],
                    centralDensitySuperStarCluster_M_sun_pc3=row[7],
                    luminositySuperStarCluster_logSun=row[8], idGalaxy=row[9]
                )
        return None

    def save(self, s_cluster: SuperStarClusterDTO) -> int:
        query = """
        INSERT INTO superStarCluster (
            idSuperStarCluster, nameSuperStarCluster, hostGalaxySuperStarCluster,
            effectiveRadiusSuperStarCluster_pc, ageSuperStarCluster_myr,
            totalMassSuperStarCluster_logSun, starFormationRateSuperStarCluster_sun_y,
            centralDensitySuperStarCluster_M_sun_pc3, luminositySuperStarCluster_logSun, idGalaxy
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(idSuperStarCluster) DO UPDATE SET
            nameSuperStarCluster=excluded.nameSuperStarCluster,
            hostGalaxySuperStarCluster=excluded.hostGalaxySuperStarCluster,
            effectiveRadiusSuperStarCluster_pc=excluded.effectiveRadiusSuperStarCluster_pc,
            ageSuperStarCluster_myr=excluded.ageSuperStarCluster_myr,
            totalMassSuperStarCluster_logSun=excluded.totalMassSuperStarCluster_logSun,
            starFormationRateSuperStarCluster_sun_y=excluded.starFormationRateSuperStarCluster_sun_y,
            centralDensitySuperStarCluster_M_sun_pc3=excluded.centralDensitySuperStarCluster_M_sun_pc3,
            luminositySuperStarCluster_logSun=excluded.luminositySuperStarCluster_logSun,
            idGalaxy=excluded.idGalaxy
        """
        with self._get_connection() as conn:
            cursor = conn.execute(query, (
                s_cluster.idSuperStarCluster, s_cluster.nameSuperStarCluster,
                s_cluster.hostGalaxySuperStarCluster, s_cluster.effectiveRadiusSuperStarCluster_pc,
                s_cluster.ageSuperStarCluster_myr, s_cluster.totalMassSuperStarCluster_logSun,
                s_cluster.starFormationRateSuperStarCluster_sun_y,
                s_cluster.centralDensitySuperStarCluster_M_sun_pc3,
                s_cluster.luminositySuperStarCluster_logSun, s_cluster.idGalaxy
            ))
            conn.commit()
            return cursor.lastrowid

    def find_all(self, limit: int = 100) -> List[SuperStarClusterDTO]:
        query = """
        SELECT idSuperStarCluster, nameSuperStarCluster, hostGalaxySuperStarCluster,
               effectiveRadiusSuperStarCluster_pc, ageSuperStarCluster_myr,
               totalMassSuperStarCluster_logSun, starFormationRateSuperStarCluster_sun_y,
               centralDensitySuperStarCluster_M_sun_pc3, luminositySuperStarCluster_logSun, idGalaxy
        FROM superStarCluster LIMIT ?
        """
        super_aglomerados = []
        with self._get_connection() as conn:
            rows = conn.execute(query, (limit,)).fetchall()
            for row in rows:
                super_aglomerados.append(SuperStarClusterDTO(
                    idSuperStarCluster=row[0], nameSuperStarCluster=row[1],
                    hostGalaxySuperStarCluster=row[2], effectiveRadiusSuperStarCluster_pc=row[3],
                    ageSuperStarCluster_myr=row[4], totalMassSuperStarCluster_logSun=row[5],
                    starFormationRateSuperStarCluster_sun_y=row[6],
                    centralDensitySuperStarCluster_M_sun_pc3=row[7],
                    luminositySuperStarCluster_logSun=row[8], idGalaxy=row[9]
                ))
        return super_aglomerados

    def delete(self, s_cluster_id: int) -> bool:
                    query = "DELETE FROM superStarCluster WHERE idSuperStarCluster = ?"
                    with self._get_connection() as conn:
                        cursor = conn.execute(query, (s_cluster_id,))
                        conn.commit()
                        return cursor.rowcount > 0
# ------------------------------------------------------------------------------------------------------------ Galáxia ----------------------------------------------------------------------
class GalaxyDAO(BaseDAO):
    def find_by_id(self, galaxy_id: int) -> Optional[GalaxyDTO]:
        query = """
        SELECT idGalaxy, nameGalaxy, hubbleTypeGalaxy, generalMorphologyGalaxy,
               distanceGalaxy_LY, effectiveRadiusGalaxy_KPC, luminosityGalaxy_logSun,
               starFormationRateGalaxy_Sun_Y, idGalaxyCluster
        FROM galaxy WHERE idGalaxy = ?
        """
        with self._get_connection() as conn:
            row = conn.execute(query, (galaxy_id,)).fetchone()
            if row:
                return GalaxyDTO(
                    idGalaxy=row[0], nameGalaxy=row[1], hubbleTypeGalaxy=row[2],
                    generalMorphologyGalaxy=row[3], distanceGalaxy_LY=row[4],
                    effectiveRadiusGalaxy_KPC=row[5], luminosityGalaxy_logSun=row[6],
                    starFormationRateGalaxy_Sun_Y=row[7], idGalaxyCluster=row[8]
                )
        return None

    def save(self, galaxy: GalaxyDTO) -> int:
        query = """
        INSERT INTO galaxy (
            idGalaxy, nameGalaxy, hubbleTypeGalaxy, generalMorphologyGalaxy,
            distanceGalaxy_LY, effectiveRadiusGalaxy_KPC, luminosityGalaxy_logSun,
            starFormationRateGalaxy_Sun_Y, idGalaxyCluster
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(idGalaxy) DO UPDATE SET
            nameGalaxy=excluded.nameGalaxy, hubbleTypeGalaxy=excluded.hubbleTypeGalaxy,
            generalMorphologyGalaxy=excluded.generalMorphologyGalaxy, distanceGalaxy_LY=excluded.distanceGalaxy_LY,
            effectiveRadiusGalaxy_KPC=excluded.effectiveRadiusGalaxy_KPC,
            luminosityGalaxy_logSun=excluded.luminosityGalaxy_logSun,
            starFormationRateGalaxy_Sun_Y=excluded.starFormationRateGalaxy_Sun_Y,
            idGalaxyCluster=excluded.idGalaxyCluster
        """
        with self._get_connection() as conn:
            cursor = conn.execute(query, (
                galaxy.idGalaxy, galaxy.nameGalaxy, galaxy.hubbleTypeGalaxy,
                galaxy.generalMorphologyGalaxy, galaxy.distanceGalaxy_LY,
                galaxy.effectiveRadiusGalaxy_KPC, galaxy.luminosityGalaxy_logSun,
                galaxy.starFormationRateGalaxy_Sun_Y, galaxy.idGalaxyCluster
            ))
            conn.commit()
            return cursor.lastrowid

    def find_all(self, limit: int = 100) -> List[GalaxyDTO]:
        query = """
        SELECT idGalaxy, nameGalaxy, hubbleTypeGalaxy, generalMorphologyGalaxy,
               distanceGalaxy_LY, effectiveRadiusGalaxy_KPC, luminosityGalaxy_logSun,
               starFormationRateGalaxy_Sun_Y, idGalaxyCluster
        FROM galaxy LIMIT ?
        """
        galaxias = []
        with self._get_connection() as conn:
            rows = conn.execute(query, (limit,)).fetchall()
            for row in rows:
                galaxias.append(GalaxyDTO(
                    idGalaxy=row[0], nameGalaxy=row[1], hubbleTypeGalaxy=row[2],
                    generalMorphologyGalaxy=row[3], distanceGalaxy_LY=row[4],
                    effectiveRadiusGalaxy_KPC=row[5], luminosityGalaxy_logSun=row[6],
                    starFormationRateGalaxy_Sun_Y=row[7], idGalaxyCluster=row[8]
                ))
        return galaxias
    
    def delete(self, galaxy_id: int) -> bool:
        query = "DELETE FROM galaxy WHERE idGalaxy = ?"
        with self._get_connection() as conn:
            cursor = conn.execute(query, (galaxy_id,))
            conn.commit()
            return cursor.rowcount > 0
# ---------------------------------------------------------------------------------------------- Aglomerado Galaxia ----------------------------------------------------------------------------
class GalaxyClusterDAO(BaseDAO):
    def find_by_id(self, g_cluster_id: int) -> Optional[GalaxyClusterDTO]:
        query = """
        SELECT idgalaxyCluster, nameGalaxyCluster, morphologyTypeGalaxyCluster,
               distanceGalaxyCluster_LY, redShiftGalaxyCluster_z, memberGalaxiesCountGalaxyCluster,
               virialRadius_Mpc, totalMassGalaxyCluster_logSun, IntraclusterGasTemp_keV,
               xRayLuminosity_erg_s, idSuperGalaxyCluster
        FROM galaxyCluster WHERE idgalaxyCluster = ?
        """
        with self._get_connection() as conn:
            row = conn.execute(query, (g_cluster_id,)).fetchone()
            if row:
                return GalaxyClusterDTO(
                    idgalaxyCluster=row[0], nameGalaxyCluster=row[1],
                    morphologyTypeGalaxyCluster=row[2], distanceGalaxyCluster_LY=row[3],
                    redShiftGalaxyCluster_z=row[4], memberGalaxiesCountGalaxyCluster=row[5],
                    virialRadius_Mpc=row[6], totalMassGalaxyCluster_logSun=row[7],
                    IntraclusterGasTemp_keV=row[8], xRayLuminosity_erg_s=row[9],
                    idSuperGalaxyCluster=row[10]
                )
        return None

    def save(self, g_cluster: GalaxyClusterDTO) -> int:
        query = """
        INSERT INTO galaxyCluster (
            idgalaxyCluster, nameGalaxyCluster, morphologyTypeGalaxyCluster,
            distanceGalaxyCluster_LY, redShiftGalaxyCluster_z, memberGalaxiesCountGalaxyCluster,
            virialRadius_Mpc, totalMassGalaxyCluster_logSun, IntraclusterGasTemp_keV,
            xRayLuminosity_erg_s, idSuperGalaxyCluster
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(idgalaxyCluster) DO UPDATE SET
            nameGalaxyCluster=excluded.nameGalaxyCluster,
            morphologyTypeGalaxyCluster=excluded.morphologyTypeGalaxyCluster,
            distanceGalaxyCluster_LY=excluded.distanceGalaxyCluster_LY,
            redShiftGalaxyCluster_z=excluded.redShiftGalaxyCluster_z,
            memberGalaxiesCountGalaxyCluster=excluded.memberGalaxiesCountGalaxyCluster,
            virialRadius_Mpc=excluded.virialRadius_Mpc,
            totalMassGalaxyCluster_logSun=excluded.totalMassGalaxyCluster_logSun,
            IntraclusterGasTemp_keV=excluded.IntraclusterGasTemp_keV,
            xRayLuminosity_erg_s=excluded.xRayLuminosity_erg_s,
            idSuperGalaxyCluster=excluded.idSuperGalaxyCluster
        """
        with self._get_connection() as conn:
            cursor = conn.execute(query, (
                g_cluster.idgalaxyCluster, g_cluster.nameGalaxyCluster,
                g_cluster.morphologyTypeGalaxyCluster, g_cluster.distanceGalaxyCluster_LY,
                g_cluster.redShiftGalaxyCluster_z, g_cluster.memberGalaxiesCountGalaxyCluster,
                g_cluster.virialRadius_Mpc, g_cluster.totalMassGalaxyCluster_logSun,
                g_cluster.IntraclusterGasTemp_keV, g_cluster.xRayLuminosity_erg_s,
                g_cluster.idSuperGalaxyCluster
            ))
            conn.commit()
            return cursor.lastrowid

    def find_all(self, limit: int = 100) -> List[GalaxyClusterDTO]:
        query = """
        SELECT idgalaxyCluster, nameGalaxyCluster, morphologyTypeGalaxyCluster,
               distanceGalaxyCluster_LY, redShiftGalaxyCluster_z, memberGalaxiesCountGalaxyCluster,
               virialRadius_Mpc, totalMassGalaxyCluster_logSun, IntraclusterGasTemp_keV,
               xRayLuminosity_erg_s, idSuperGalaxyCluster
        FROM galaxyCluster LIMIT ?
        """
        aglomerados_galaxias = []
        with self._get_connection() as conn:
            rows = conn.execute(query, (limit,)).fetchall()
            for row in rows:
                aglomerados_galaxias.append(GalaxyClusterDTO(
                    idgalaxyCluster=row[0], nameGalaxyCluster=row[1],
                    morphologyTypeGalaxyCluster=row[2], distanceGalaxyCluster_LY=row[3],
                    redShiftGalaxyCluster_z=row[4], memberGalaxiesCountGalaxyCluster=row[5],
                    virialRadius_Mpc=row[6], totalMassGalaxyCluster_logSun=row[7],
                    IntraclusterGasTemp_keV=row[8], xRayLuminosity_erg_s=row[9],
                    idSuperGalaxyCluster=row[10]
                ))
        return aglomerados_galaxias

    def delete(self, g_cluster_id: int) -> bool:
            query = "DELETE FROM galaxyCluster WHERE idGalaxyCluster = ?"
            with self._get_connection() as conn:
                cursor = conn.execute(query, (g_cluster_id,))
                conn.commit()
                return cursor.rowcount > 0
# ------------------------------------------------------------------------------------------ SuperAglomerado Estrelar --------------------------------------------------------------------------------
class SuperGalaxyClusterDAO(BaseDAO):
    def find_by_id(self, sg_cluster_id: int) -> Optional[SuperGalaxyClusterDTO]:
        query = """
        SELECT idSuperGalaxyCluster, nameSuperGalaxyCluster, cosmicStructureTypeSuperGalaxyCluster,
               distanceSuperGalaxyCluster_Mpc, redshiftSuperGalaxyCluster_z, memberClustersCount,
               extentLength_Mpc, totalMassGalaxyCluster_logSun, overdensityFactor
        FROM superGalaxyCluster WHERE idSuperGalaxyCluster = ?
        """
        with self._get_connection() as conn:
            row = conn.execute(query, (sg_cluster_id,)).fetchone()
            if row:
                return SuperGalaxyClusterDTO(
                    idSuperGalaxyCluster=row[0], nameSuperGalaxyCluster=row[1],
                    cosmicStructureTypeSuperGalaxyCluster=row[2], distanceSuperGalaxyCluster_Mpc=row[3],
                    redshiftSuperGalaxyCluster_z=row[4], memberClustersCount=row[5],
                    extentLength_Mpc=row[6], totalMassGalaxyCluster_logSun=row[7],
                    overdensityFactor=row[8]
                )
        return None

    def save(self, sg_cluster: SuperGalaxyClusterDTO) -> int:
        query = """
        INSERT INTO superGalaxyCluster (
            idSuperGalaxyCluster, nameSuperGalaxyCluster, cosmicStructureTypeSuperGalaxyCluster,
            distanceSuperGalaxyCluster_Mpc, redshiftSuperGalaxyCluster_z, memberClustersCount,
            extentLength_Mpc, totalMassGalaxyCluster_logSun, overdensityFactor
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(idSuperGalaxyCluster) DO UPDATE SET
            nameSuperGalaxyCluster=excluded.nameSuperGalaxyCluster,
            cosmicStructureTypeSuperGalaxyCluster=excluded.cosmicStructureTypeSuperGalaxyCluster,
            distanceSuperGalaxyCluster_Mpc=excluded.distanceSuperGalaxyCluster_Mpc,
            redshiftSuperGalaxyCluster_z=excluded.redshiftSuperGalaxyCluster_z,
            memberClustersCount=excluded.memberClustersCount,
            extentLength_Mpc=excluded.extentLength_Mpc,
            totalMassGalaxyCluster_logSun=excluded.totalMassGalaxyCluster_logSun,
            overdensityFactor=excluded.overdensityFactor
        """
        with self._get_connection() as conn:
            cursor = conn.execute(query, (
                sg_cluster.idSuperGalaxyCluster, sg_cluster.nameSuperGalaxyCluster,
                sg_cluster.cosmicStructureTypeSuperGalaxyCluster, sg_cluster.distanceSuperGalaxyCluster_Mpc,
                sg_cluster.redshiftSuperGalaxyCluster_z, sg_cluster.memberClustersCount,
                sg_cluster.extentLength_Mpc, sg_cluster.totalMassGalaxyCluster_logSun,
                sg_cluster.overdensityFactor
            ))
            conn.commit()
            return cursor.lastrowid

    def find_all(self, limit: int = 100) -> List[SuperGalaxyClusterDTO]:
        query = """
        SELECT idSuperGalaxyCluster, nameSuperGalaxyCluster, cosmicStructureTypeSuperGalaxyCluster,
               distanceSuperGalaxyCluster_Mpc, redshiftSuperGalaxyCluster_z, memberClustersCount,
               extentLength_Mpc, totalMassGalaxyCluster_logSun, overdensityFactor
        FROM superGalaxyCluster LIMIT ?
        """
        super_aglomerados_galaxias = []
        with self._get_connection() as conn:
            rows = conn.execute(query, (limit,)).fetchall()
            for row in rows:
                super_aglomerados_galaxias.append(SuperGalaxyClusterDTO(
                    idSuperGalaxyCluster=row[0], nameSuperGalaxyCluster=row[1],
                    cosmicStructureTypeSuperGalaxyCluster=row[2], distanceSuperGalaxyCluster_Mpc=row[3],
                    redshiftSuperGalaxyCluster_z=row[4], memberClustersCount=row[5],
                    extentLength_Mpc=row[6], totalMassGalaxyCluster_logSun=row[7],
                    overdensityFactor=row[8]
                ))
        return super_aglomerados_galaxias

    def delete(self, sg_cluster_id: int) -> bool:
                query = "DELETE FROM superGalaxyCluster WHERE idSuperGalaxyCluster = ?"
                with self._get_connection() as conn:
                    cursor = conn.execute(query, (sg_cluster_id,))
                    conn.commit()
                    return cursor.rowcount > 0